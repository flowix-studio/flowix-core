# -*- coding: utf-8 -*-
from flowix import (
    Workspace, Workflow,
    StartNode,
    IfNode, ForNode, WhileNode, BreakNode,
    ExecNode,
    DataframeNode,
    DatabaseNode,
    ScriptNode,
    DebugNode
)

ws = Workspace()
wf = Workflow(ws)

for cls in ( StartNode, IfNode, ForNode, WhileNode, BreakNode, ExecNode, DataframeNode, DatabaseNode, ScriptNode, DebugNode ):
    n = cls(wf)

print(ws.info())
