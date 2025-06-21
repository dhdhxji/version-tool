import argparse as ap
import json
from dataclasses import dataclass, asdict
from string import Template

@dataclass
class Version:
    major: int
    minor: int
    patch: int

arg_parser = ap.ArgumentParser()
arg_parser.add_argument('action', type=str, choices=['template', 'increment'], help='Action to perform')
arg_parser.add_argument('--version-file', type=str, help='version.json file location')
arg_parser.add_argument('--template', type=str, help='Template file location')
arg_parser.add_argument('--output', type=str, help='Template output location')

args = arg_parser.parse_args()

if args.action == 'template':
    with open(args.version_file) as f:
        version = json.load(f)
    version = Version(**version)
    
    with open(args.template) as f:
        template = f.read()
    template = Template(template)
    
    
    with open(args.output, 'w') as f:
        f.write(template.substitute(asdict(version)))

elif args.action == 'increment':
    with open(args.version_file) as f:
        version = json.load(f)
    version = Version(**version)

    version.patch += 1
    with open(args.version_file, 'w') as f:
        json.dump(asdict(version), f, indent=4)
        f.write('\n')
