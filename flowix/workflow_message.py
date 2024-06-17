# -*- coding: utf-8 -*-
from dataclasses import dataclass, field


@dataclass
class WorkflowMessage:
    id:str
    cond_state:dict = field(default_factory = dict)
    payload:dict = field(default_factory = dict)
    
    @staticmethod
    def new(id:str) -> "WorkflowMessage":
        return WorkflowMessage(
            id = id,
            cond_state = { "loop_break": False },
            payload = {}
        )
