import argparse as ap
import json
from dataclasses import dataclass, asdict
from string import Template
import subprocess
import hashlib
import os

@dataclass
class Version:
    major: int
    minor: int
    patch: int

@dataclass
class GitInfo:
    author_name: str
    author_email: str
    commit_hash: str
    commit_msg: str
    dirty: bool
    describe: str
    user_name: str
    user_email: str

arg_parser = ap.ArgumentParser()
arg_parser.add_argument('action', type=str, choices=['template', 'increment', 'update-git-state-file'], help='Action to perform')
arg_parser.add_argument('--version-file', type=str, help='version.json file location')
arg_parser.add_argument('--template', type=str, help='Template file location')
arg_parser.add_argument('--output', type=str, help='Template output location')
arg_parser.add_argument('--git-exec', type=str, default='git', help='Git executable path')
arg_parser.add_argument('--repo-path', type=str, help='Git repository location')
arg_parser.add_argument('--git-state-path', type=str, help='Git state file location (useful for build systems to keep track of). Note: it must be outside of git tree (or git ignored) to detect repo changes properly')

args = arg_parser.parse_args()



def run_git_command(cwd: str, git_exec: str, *args) -> str:
    result = subprocess.run((git_exec, *args), capture_output=True, cwd=cwd)

    if result.returncode != 0:
        raise Exception(f'`git {" ".join(args)}` failed with return code {result.returncode}:\n{result.stderr.decode()}')

    return result.stdout.decode()


git = lambda *git_args: run_git_command(args.repo_path, args.git_exec, *git_args)

def git_state() -> str:
    git1 = lambda *args: f'git {" ".join(args)}\n{git(*args)}\n'

    state = ''
    state += git1('rev-parse', 'HEAD')
    state += git1('status', '--porcelain')
    state += git1('diff', '--shortstat')

    state += 'git --no-pager diff --no-color | sha1sum\n'
    git_diff_output = git('--no-pager', 'diff', '--no-color')
    state += hashlib.sha1(git_diff_output.encode()).hexdigest()
    state += '\n'

    return state

def git_info() -> GitInfo:
    return GitInfo(
        git('show', '-s', '--format=%an', 'HEAD').strip(),          # commit author name
        git('show', '-s', '--format=%ae', 'HEAD').strip(),          # commit author email
        git('show', '-s', '--format=%H', 'HEAD').strip(),           # commit hash
        git('show', '-s', '--format=%s', 'HEAD').strip(),           # commit subject
        1 if git('status', '--porcelain').strip() != '' else 0,     # dirty
        git('describe', '--always', '--dirty').strip(),
        git('config', '--default', '"unknown"', '--get', 'user.name').strip(),
        git('config', '--default', '"unknown"', '--get', 'user.email').strip()
    )


if args.action == 'template':
    with open(args.version_file) as f:
        version = json.load(f)
    version = Version(**version)

    with open(args.template) as f:
        template = f.read()
    template = Template(template)
    
    with open(args.output, 'w') as f:
        f.write(template.substitute(
            { **asdict(version), **asdict(git_info())}
        ))

elif args.action == 'increment':
    with open(args.version_file) as f:
        version = json.load(f)
    version = Version(**version)

    version.patch += 1
    with open(args.version_file, 'w') as f:
        json.dump(asdict(version), f, indent=4)
        f.write('\n')

elif args.action == 'update-git-state-file':
    git_state = git_state()

    if os.path.exists(args.git_state_path):
        with open(args.git_state_path) as f:
            old_git_state = f.read()
    else:
        old_git_state = ''

    if git_state != old_git_state:
        print('Git state has been updated:')
        print(git_state)

        with open(args.git_state_path, 'w') as f:
            f.write(git_state)

