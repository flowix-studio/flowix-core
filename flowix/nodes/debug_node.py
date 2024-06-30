# -*- coding: utf-8 -*-
import json, pprint
from ..node import Node, NodeParameters
from ..workflow_message import WorkflowMessage


class DebugNodeParameters(NodeParameters):
    """
    Parameters
    - object: object to debug(message, message.payload / default: message.payload)
    - indent: indent size for pretty print(default: 4)
    """
    object:str
    indent:int

class DebugNode(Node):
    """
    Node for print log to console
    """
    def __init__(self, workflow = None, node_id:str = None, node_name:str = None):
        super().__init__(workflow, node_id, node_name, [ "input" ], [], {
            "object": { "type": "str", "default": "message.payload" },
            "indent": { "type": "int", "default": 4 }
        })

    @property
    def parameters(self) -> DebugNodeParameters:
        return super().parameters


    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        if self.parameters.object == "message":
            print(message)
        else:
            try:
                object = eval(self.parameters.object)
            except:
                raise ValueError("invalid object!")

            try:
                print(json.dumps(object, indent = self.parameters.indent))
            except:
                pprint.pp(object, indent = self.parameters.indent)

        return message

    def to_script(self) -> str:
        return super().to_script()
