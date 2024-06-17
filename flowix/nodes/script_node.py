# -*- coding: utf-8 -*-
from ..node import Node
from ..workflow_message import WorkflowMessage


class ScriptNode(Node):
    """
    Node for execute python script
    """
    def __init__(self, workflow, node_id:str = None, node_name:str = None):
        """
        Parameters
        - script: script to execute
        """
        super().__init__(workflow, node_id, node_name, [ "input" ], [ "output" ], { "script": "# type code below\nreturn message" })
        
    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        exec("""
def fn_compute(message):
""" + "\n".join([
    "\t" + line.strip()
    for line in self.parameters["script"].split("\n")
    if not line.strip() == ""
]))
        
        m = eval("fn_compute")(message)
        if m is None:
            return message
        else:
            return m
