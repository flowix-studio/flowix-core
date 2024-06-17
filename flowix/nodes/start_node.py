# -*- coding: utf-8 -*-
from ..node import Node
from ..workflow_message import WorkflowMessage


class StartNode(Node):
    """
    Node for start point of Workflow
    """
    def __init__(self, workflow, node_id:str = None, node_name:str = None):
        """
        Parameters
        - payload: initial payload data to update into message.payload
        """
        super().__init__(workflow, node_id, node_name, [], [ "output" ], { "payload": {} })
        
    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        message.payload.update(self.parameters["payload"])

        return message
