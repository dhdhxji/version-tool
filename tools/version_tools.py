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
arg_parser.add_argument('version_file', type=str, help='version.json file location')
arg_parser.add_argument('template', type=str, help='version.json file location')
arg_parser.add_argument('output', type=str, help='version.json file location')

args = arg_parser.parse_args()

with open(args.version_file) as f:
    version = json.load(f)
version = Version(**version)

with open(args.template) as f:
    template = f.read()
template = Template(template)


with open(args.output, 'w') as f:
    f.write(template.substitute(asdict(version)))
