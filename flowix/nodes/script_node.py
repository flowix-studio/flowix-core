# -*- coding: utf-8 -*-
from ..node import Node, NodeParameters
from ..workflow_message import WorkflowMessage


class ScriptNodeParameters(NodeParameters):
    """
    Parameters
    - script: script to execute
    """
    script:str

class ScriptNode(Node):
    """
    Node for execute python script
    """
    def __init__(self, workflow = None, node_id:str = None, node_name:str = None):
        super().__init__(workflow, node_id, node_name, [ "input" ], [ "output" ], {
            "script": { "type": str, "default": "# type code below\nreturn message"}
        })

    @property
    def parameters(self) -> ScriptNodeParameters:
        return super().parameters


    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        exec("""
def fn_compute(message):
""" + "\n".join([
    "\t" + line.strip()
    for line in self.parameters.script.split("\n")
    if not line.strip() == ""
]))

        m = eval("fn_compute")(message)
        if m is None:
            return message
        else:
            return m

    def to_script(self) -> str:
        return super().to_script()
