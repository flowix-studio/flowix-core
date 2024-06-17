# -*- coding: utf-8 -*-
import os, argparse, shutil
from .workspace import Workspace


def run_cli():
    # argument parser
    parser = argparse.ArgumentParser()
    # subparser(command)
    command = parser.add_subparsers(dest = "command")
    # create
    cmd_create = command.add_parser("create", help = "create flowix workspace")
    cmd_create.add_argument("path", help = "directory path to create flowix workspace")
    cmd_create.add_argument("--id", default = None, help = "workspace id")
    cmd_create.add_argument("--name", default = None, help = "workspace name")
    # run
    cmd_run = command.add_parser("run", help = "run flowix workspace")
    cmd_run.add_argument("--workflow", default = "all", help = "execution mode(default: all)")
    # delete
    cmd_run = command.add_parser("delete", help = "delete flowix workspace")
    # parse args
    args = parser.parse_args()
    
    
    # create
    if args.command == "create":
        Workspace.create(args.path, args.id, args.name)
    elif args.command == "run":
        # load workspace and run
        Workspace.load(os.getcwd()).execute(args.workflow)
    elif args.command == "delete":
        shutil.rmtree(os.getcwd())


if __name__ == "__main__":
    run_cli()
