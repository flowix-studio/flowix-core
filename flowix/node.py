# -*- coding: utf-8 -*-
import uuid, copy, codecs, pickle
from typing import Any, Literal
from .workflow_message import WorkflowMessage


class NodeInput:
    def __init__(self, node:"Node", name:str):
        self.__node, self.__name = node, name
        
    @property
    def node(self) -> "Node":
        return self.__node
    
    @property
    def name(self) -> str:
        return self.__name

class NodeOutput:
    def __init__(self, node:"Node", name:str):
        self.__node, self.__name = node, name
        self.__enabled = True
        self.__connections:list[NodeInput] = []
        
    @property
    def node(self) -> "Node":
        return self.__node
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def enabled(self) -> bool:
        return self.__enabled
    
    @enabled.setter
    def enabled(self, state:bool):
        self.__enabled = state
    
    @property
    def connections(self) -> list[NodeInput]:
        return [
            item
            for item in self.__connections
        ]


    def connect(self, node_input:NodeInput):
        if not isinstance(node_input, NodeInput):
            raise TypeError("NodeOutput can connect with NodeInput only!")

        if not node_input in self.__connections:
            self.__connections.append(node_input)
            
    def disconnect(self, node_input:NodeInput):
        self.__connections.remove(node_input)
            
    def clear(self):
        self.__connections.clear()

class NodeParameters:
    def __init__(self, parameter_info:dict[str, type | dict[Literal["type", "default"], Any]]):
        self.__param_info = {}
        for name, info in parameter_info.items():
            if isinstance(info, type):
                self.__param_info[name] = info
                setattr(self, name, None)
            elif isinstance(info, dict):
                self.__param_info[name] = info["type"]
                setattr(self, name, info["default"])

    @property
    def info(self) -> dict[str, type | dict[Literal["type", "default"], type | Any]]:
        return self.__param_info


class Node:
    has_iter = False

    def __init__(self, workflow, node_id:str = None, node_name:str = None, inputs:list[str] = [ "input" ], outputs:list[str] = [ "output" ], parameters:dict[str, type | dict[Literal["type", "default"], Any]] = {}):
        self.__workflow = workflow
        self.__node_id = uuid.uuid4().hex[:5] if node_id is None else node_id
        self.__name = f"{self.__class__.__name__}_{self.__node_id}" if node_name is None else node_name

        self.__parameters:NodeParameters = NodeParameters(parameters)
        self.__init_parameters = copy.deepcopy(self.__parameters)
        self.__inputs = {
            input_name: NodeInput(self, input_name)
            for input_name in inputs
        }
        self.__outputs = {
            output_name: NodeOutput(self, output_name)
            for output_name in outputs
        }

        workflow.append_node(self)

    @property
    def workflow(self):
        return self.__workflow

    @property
    def id(self) -> str:
        return self.__node_id

    @id.setter
    def id(self, new_id:str):
        self.__node_id = new_id

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, new_name:str):
        self.__name = new_name

    @property
    def parameters(self) -> NodeParameters:
        return self.__parameters

    @property
    def inputs(self) -> dict[str, NodeInput]:
        return self.__inputs

    @property
    def outputs(self) -> dict[str, NodeOutput]:
        return self.__outputs


    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        return message

    def reset_parameters(self):
        self.__parameters = copy.deepcopy(self.__init_parameters)

    def copy(self, reset_parameters:bool = True) -> "Node":
        copied_node = copy.deepcopy(self)
        if reset_parameters:
            copied_node.reset_parameters()

        return copied_node

    def to_script(self, include_parameters_info:bool = False, include_extra_args = False, import_string:str = None) -> str:
        if include_parameters_info:
            if include_extra_args:
                define_string = f'{self.name} = {self.__class__.__name__}({self.__workflow.name}, "{self.id}", "{self.name}", {list(self.inputs.keys())}, {list(self.outputs.keys())}, {self.parameters.info})'
            else:
                define_string = f'{self.name} = {self.__class__.__name__}({self.__workflow.name}, "{self.id}", "{self.name}", parameters = {self.parameters.info})'
        else:
            if include_extra_args:
                define_string = f'{self.name} = {self.__class__.__name__}({self.__workflow.name}, "{self.id}", "{self.name}", {list(self.inputs.keys())}, {list(self.outputs.keys())})'
            else:
                define_string = f'{self.name} = {self.__class__.__name__}({self.__workflow.name}, "{self.id}", "{self.name}")'
        
        parameter_string = ""
        for name, info in self.parameters.info.items():
            param_value = getattr(self.parameters, name)
            if param_value is not None:
                if isinstance(info, dict):
                    if info["type"] == str or isinstance(param_value, str):
                        parameter_string += f'\n{self.name}.parameters.{name} = """{param_value}"""'
                    else:
                        parameter_string += f'\n{self.name}.parameters.{name} = {param_value}'
                elif isinstance(info, type):
                    if info == str or isinstance(param_value, str):
                        parameter_string += f'\n{self.name}.parameters.{name} = """{param_value}"""'
                    else:
                        parameter_string += f'\n{self.name}.parameters.{name} = {param_value}'

        if parameter_string != "":
            parameter_string = "\n# parameters" + parameter_string

        if import_string is None:
            return f"# Node {self.name} Script\nfrom flowix import {self.__class__.__name__}\n" + define_string + parameter_string + "\n"
        else:
            return f"# Node {self.name} Script\n{import_string}\n" + define_string + parameter_string + "\n"

    # serialize/deserialize from codecs string
    def serialize(self) -> str:
        return codecs.encode(pickle.dumps(self), "base64").decode()

    @staticmethod
    def deserialize(source:str) -> "Node":
        return pickle.loads(codecs.decode(source.encode(), "base64"))
