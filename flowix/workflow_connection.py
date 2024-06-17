# -*- coding: utf-8 -*-
import json


class WorkflowConnection(list):
    def __init__(self, workflow, connections:list):
        super().__init__(tuple(connections))
        
        self.__workflow_id = workflow.id
        
    def pprint(self, indent = 4):
        print(f"[Connections of Workflow({self.__workflow_id})]\n{json.dumps(self, indent = indent)}")
