import argparse as ap

arg_parser = ap.ArgumentParser()
arg_parser.add_argument('--version_file', type=str, help='version.json file location')

args = arg_parser.parse_args()

with open(args.version_file) as f:
    print(f.read())

with open('version.h', 'w') as f:
    f.write('#define VERSION "1.2.3.4"\n')
