# -*- coding: utf-8 -*-
import json, pprint, pandas as pd
from ..node import Node
from ..workflow_message import WorkflowMessage


class DebugNode(Node):
    """
    Node for print log to console
    """
    def __init__(self, workflow, node_id:str = None, node_name:str = None):
        """
        Parameters
        - object: object to debug(message, message.payload / default: message.payload)
        - indent: indent size for pretty print(default: 4)
        """
        super().__init__(workflow, node_id, node_name, [ "input" ], [], { "object": "message.payload", "indent": 4 })

    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        if self.parameters["object"] == "message":
            print(message)
        else:
            try:
                object = eval(self.parameters["object"])
            except:
                raise ValueError("invalid object!")
            
            try:
                print(json.dumps(object, indent = self.parameters["indent"]))
            except:
                pprint.pp(object, indent = self.parameters["indent"])
                
        return message
