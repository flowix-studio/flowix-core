# -*- coding: utf-8 -*-
import modin.pandas, pandas
from ..node import Node
from ..workflow_message import WorkflowMessage


class IfNode(Node):
    """
    Node for checking cond
    """
    def __init__(self, workflow, node_id:str = None, node_name:str = None):
        """
        Parameters
        - source: name of source from message.payload
        - separator: comparison separator("==", "!=", "is", "is not", ">", "<" ... / default: "==")
        - target: comparison target
        """
        super().__init__(workflow, node_id, node_name, [ "input" ], [ "output1", "output2" ], {
            "source": None,
            "separator": "==",
            "target": None
        })

    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        source_name = self.parameters["source"]
        if source_name is None:
            raise ValueError("`source` must be specified!")
        
        try:
            source = message.payload[source_name]
        except KeyError:
            raise KeyError("invalid source name!")
        
        cond_result = eval(f"source {self.parameters['separator']} self.parameters['target']")
        self.outputs["output1"].enabled = cond_result
        self.outputs["output2"].enabled = not cond_result

        return message

class ForNode(Node):
    """
    Node for looping
    """
    has_iter = False

    def __init__(self, workflow, node_id:str = None, node_name:str = None):
        """
        Parameters
        - variable_name: key used to save current iterable set in message.payload(default: for_iter)
        - mode: iterable select/create mode(payload, manual / default: payload)
        - index: include index or not(default: False)
        - max_iter: max iteration number for loop(default: None)
        - for `manual` mode
            - source: name of iterable from message.payload
        - for `manual` mode
            - iterable: manual iterable
        """
        super().__init__(workflow, node_id, node_name, [ "input" ], [ "output" ], {
            "variable_name": "for_iter",
            "mode": "payload",
            "index": False,
            "max_iter": None,
            "source": None,
            "iterable": []
        })

    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        if self.parameters["mode"] == "payload":
            try:
                iterable = message.payload[self.parameters["source"]]
                if isinstance(iterable, modin.pandas.DataFrame) or isinstance(iterable, pandas.DataFrame):
                    iterable = iterable.to_dict(orient = "records")
            except KeyError:
                raise KeyError("invalie source key!")
        else:
            iterable = self.parameters["iterable"]
            
        def check_break() -> bool:
            if self.workflow.state == "idle" or message is None:
                return True
            if message.cond_state["loop_break"]:
                return True

            return False
        
        max_iter = self.parameters["max_iter"]
        for iter_item in enumerate(iterable):
            if check_break():
                break
            
            if max_iter is not None and iter_item[0] + 1 > max_iter:
                break

            message.payload[self.parameters["variable_name"]] = iter_item if self.parameters["index"] else iter_item[1]

            for node_output in self.outputs.values():
                if check_break():
                    break

                for node_input in node_output.connections:
                    if check_break():
                        break

                    message = self.workflow.execute_single_node(message.id, message, node_input.node, self, nested = message.payload["is_nested_workflow"])

        return message

class WhileNode(Node):
    """
    Node for while loop
    """
    has_iter = False

    def __init__(self, workflow, node_id:str = None, node_name:str = None):
        super().__init__(workflow, node_id, node_name, [ "input" ], [ "output" ])

    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        def check_break() -> bool:
            if self.workflow.state == "idle" or message is None:
                return True
            if message.cond_state["loop_break"]:
                return True

            return False
        
        while True:
            # print(message.payload)

            if check_break():
                break

            for node_output in self.outputs.values():
                if check_break():
                    break

                for node_input in node_output.connections:
                    if check_break():
                        break

                    message = self.workflow.execute_single_node(message.id, message, node_input.node, self, nested = message.payload["is_nested_workflow"])

        return message

class BreakNode(Node):
    """
    Node for break for loop node
    """
    def __init__(self, workflow, node_id:str = None, node_name:str = None):
        super().__init__(workflow, node_id, node_name, [ "input" ], [ "output" ])

    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        message.cond_state["loop_break"] = True

        return message
