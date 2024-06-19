# -*- coding: utf-8 -*-
from ..node import Node, NodeParameters
from ..workflow_message import WorkflowMessage


class StartNodeParameters(NodeParameters):
    """
    Parameters
    - payload: initial payload data to update into message.payload
    """
    payload:dict

class StartNode(Node):
    """
    Node for start point of Workflow
    """
    def __init__(self, workflow, node_id:str = None, node_name:str = None):
        super().__init__(workflow, node_id, node_name, [], [ "output" ], { "payload": { "type": dict, "default": {} } })

    @property
    def parameters(self) -> StartNodeParameters:
        return super().parameters

        
    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        message.payload.update(self.parameters.payload)

        return message

    def to_script(self) -> str:
        return super().to_script()
