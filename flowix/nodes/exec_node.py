# -*- coding: utf-8 -*-
import subprocess
from ..node import Node
from ..workflow_message import WorkflowMessage


class ExecNode(Node):
    """
    Node to execute batch(shell) script or external program
    """
    def __init__(self, workflow, node_id:str = None, node_name:str = None):
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
        super().__init__(workflow, node_id, node_name, [ "input" ], [ "output" ], {
            "variable_name": "exec_result",
            "mode": "shell",
            "command": None,
            "target": None,
            "arguments": None
        })
        
    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        if self.parameters["mode"] == "shell":
            exec_args = self.parameters["command"].split(" ")
        elif self.parameters["mode"] == "program":
            exec_args = [ self.parameters["target"] ] + self.parameters["arguments"].split(" ")
            
        message.payload[self.parameters["variable_name"]] = [
            item.strip()
            for item in subprocess.check_output(exec_args, shell = True, stderr = subprocess.STDOUT).decode().split("\n")
            if not item.strip() == ""
        ]
        
        return message
