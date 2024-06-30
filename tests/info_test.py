# -*- coding: utf-8 -*-
from flowix import (
    StartNode,
    IfNode, ForNode, WhileNode, BreakNode,
    ExecNode,
    DataframeNode,
    DatabaseNode,
    ScriptNode,
    DebugNode
)

for cls in ( StartNode, IfNode, ForNode, WhileNode, BreakNode, ExecNode, DataframeNode, DatabaseNode, ScriptNode, DebugNode ):
    n = cls()
    print(n.info())
