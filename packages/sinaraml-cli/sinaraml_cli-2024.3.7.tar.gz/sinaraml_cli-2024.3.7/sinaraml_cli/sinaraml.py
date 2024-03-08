#!/usr/bin/env python3

import argparse
import logging


def jupyter_cli_init(root_parser):
    try:
        from sinaraml_cli_jupyter import init_cli
        init_cli(root_parser)
    except Exception as e:
        pass

def host_cli_init(root_parser):
    try:
        from sinaraml_cli_host import init_cli
        init_cli(root_parser)
    except Exception as e:
        pass  

def get_jupyter_cli_subjects():
    try:
        from sinaraml_cli_jupyter import get_subjects
        return get_subjects()
    except Exception as e:
        pass
    return []

def get_host_cli_subjects():
    try:
        from sinaraml_cli_host import get_subjects
        return get_subjects()
    except Exception as e:
        pass
    return []

def setup_logging(use_vebose=False):
    logging.basicConfig(format="%(levelname)s: %(message)s")
    if use_vebose:
        logging.getLogger().setLevel(logging.DEBUG)

def main():

    exit_code = -1

    # populate list of avalilable cli plugins for help strings
    available_cli = [ *get_host_cli_subjects(), *get_jupyter_cli_subjects() ]
    available_cli_list = ",".join(available_cli)

    if not available_cli:
        print('No CLI plugins installed, to install use:\n\nOn your host system: pip install sinaraml_cli_host\ninside your sinara server: pip install sinaraml_cli_jupyter\n')
        return exit_code

    # add root parser and root subcommand parser (subject)
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subject', dest='subject', help=f"subject to use [{available_cli_list}]")
    parser.add_argument('-v', '--verbose', action='store_true', help="display verbose logs")

    # each cli plugin adds and manages subcommand handlers (starting from subject handler) to root parser
    host_cli_init(subparsers)
    jupyter_cli_init(subparsers)

    # parse the command line and get all arguments
    args = parser.parse_args()

    # Setup logs format and verbosity level
    setup_logging(args.verbose)
    
    # display help if required arguments are missing
    if not args.subject:
        parser.print_help()
    elif not args.action:
        subparsers_actions = [
            action for action in parser._actions 
            if isinstance(action, argparse._SubParsersAction)]
        for subparsers_action in subparsers_actions:
            for choice, subparser in subparsers_action.choices.items():
                if args.subject == choice:
                    print(subparser.format_help())

    # call appropriate handler for the whole command line from a cli plugin if installed
    if hasattr(args, 'func'):
        try:
            args.func(args)
            exit_code = 0
        except Exception as e:
            logging.error(e)
    
    return exit_code

if __name__ == "__main__":
    main()