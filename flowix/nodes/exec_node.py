# -*- coding: utf-8 -*-
import subprocess
from typing import Literal
from ..node import Node, NodeParameters
from ..workflow_message import WorkflowMessage


class ExecNodeParameters(NodeParameters):
    """
    Parameters
    - variable_name: key used to save results in message.payload(default: exec_result)
    - mode: execution mode(shell, program / default: shell)
    - for `shell` mode
        - command: cmd command
    - for `program` mode
        - target: target program
        - arguments: additional arguments
    """
    variable_name:str
    mode:Literal["shell", "program"]
    # for shell
    commands:list
    # for program
    target:str
    arguments:list

class ExecNode(Node):
    """
    Node to execute batch(shell) script or external program
    """
    def __init__(self, workflow = None, node_id:str = None, node_name:str = None):
        super().__init__(workflow, node_id, node_name, [ "input" ], [ "output" ], {
            "variable_name": { "type": str, "default": "exec_result"},
            "mode": { "type": str, "default": "shell"},
            "command": list,
            "target": str,
            "arguments": list
        })

    @property
    def parameters(self) -> ExecNodeParameters:
        return super().parameters


    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        if self.parameters.mode == "shell":
            exec_args = self.parameters.commands
        elif self.parameters.mode == "program":
            exec_args = [ self.parameters.target ] + self.parameters.arguments

        message.payload[self.parameters.variable_name] = [
            item.strip()
            for item in subprocess.check_output(exec_args, shell = True, stderr = subprocess.STDOUT).decode().split("\n")
            if not item.strip() == ""
        ]

        return message

    def to_script(self) -> str:
        return super().to_script()
