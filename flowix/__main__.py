# -*- coding: utf-8 -*-
import argparse
from .workspace import Workspace


def run_cli():
    # argument parser
    parser = argparse.ArgumentParser()
    # subparser(command)
    command = parser.add_subparsers(dest = "command")
    # create
    cmd_create = command.add_parser("create", help = "create flowix workspace")
    cmd_create.add_argument("file", help = "file path of workspace")
    cmd_create.add_argument("--id", default = None, help = "workspace id")
    cmd_create.add_argument("--name", default = None, help = "workspace name")
    # run
    cmd_run = command.add_parser("run", help = "run flowix workspace")
    cmd_run.add_argument("file", help = "file path of workspace")
    cmd_run.add_argument("--workflow", default = "all", help = "execution mode(default: all)")
    # parse args
    args = parser.parse_args()
    
    
    # create
    if args.command == "create":
        Workspace.create(args.file, args.id, args.name)
    elif args.command == "run":
        # load workspace and run
        Workspace.load(args.file).execute(args.workflow)


if __name__ == "__main__":
    run_cli()
