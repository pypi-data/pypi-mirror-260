import argparse
import os

import colorama

from . import read_journals
from . import stat_groups
from .stat_groups import *
from .colors import TITLE, STAT, RESET

PROGRAM_NAME = "explorer-stats"
VERSION = "1.0.1"


def main():
    colorama.init(autoreset=True)

    parser = build_arg_parser()
    
    args = parser.parse_args()
    
    if not args.stat_group:
        run_main()
    else:
        stat_group_name = args.stat_group
        if stat_group_name not in stat_groups.get_module_names():
            invalid_stat_group(stat_group_name)
        else:
            run_stat_group(args)


def run_stat_group(args):
    module = stat_groups.get_module(args.stat_group)
    collector = module.new_collector()
    
    saves_path = os.path.expandvars(args.saves_path)

    for event in read_journals.read_events(saves_path, args.exclude_legacy):
        collector.process_event(event)
    
    print(collector.get_output())


def invalid_stat_group(name):
    print(f"Invalid stat group '{name}', probably missing in package init file")


def run_main():
    print_stat_groups()


def print_stat_groups():
    for name in stat_groups.get_module_names(): 
        print(f"{TITLE}{name}{RESET} - {STAT}{stat_groups.get_module(name).get_description()}")


def build_arg_parser():
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME)
    parser.add_argument("--saves_path", type=str,
                        default="%USERPROFILE%/Saved Games/Frontier Developments/Elite Dangerous",
                        help="path to the ED saved data")
    parser.add_argument("--version", action="version", version=f"{PROGRAM_NAME} v{VERSION}")
    parser.add_argument("-xl", "--exclude-legacy", "--no-legacy", action="store_true",
                        help="Exclude legacy journal files from stats", dest="exclude_legacy")
    
    subparsers = parser.add_subparsers(dest="stat_group")
    
    for name in stat_groups.get_module_names():
        subparser = subparsers.add_parser(name)
        
        stat_groups.get_module(name).setup_parser(subparser)
    
    return parser

    
if __name__ == "__main__":
    main()
