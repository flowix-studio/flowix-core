# -* coding: utf-8 -*-
# Automatically Exported Script of Flowix Workspace

##### Workspace Workspace_ec02c4f7838544e690408e427d8244fe Script
from flowix import Workspace
Workspace_ec02c4f7838544e690408e427d8244fe = Workspace("ec02c4f7838544e690408e427d8244fe", "Workspace_ec02c4f7838544e690408e427d8244fe")

#### workflows
### Workflow Workflow_71829 Script
from flowix import Workflow
Workflow_71829 = Workflow(Workspace_ec02c4f7838544e690408e427d8244fe, "71829", "Workflow_71829")
## nodes
# Node StartNode_6f827 Script
from flowix import StartNode
StartNode_6f827 = StartNode(Workflow_71829, "6f827", "StartNode_6f827")
# parameters
StartNode_6f827.parameters.payload = {'num': 0}
# Node WhileNode_c7d06 Script
from flowix import WhileNode
WhileNode_c7d06 = WhileNode(Workflow_71829, "c7d06", "WhileNode_c7d06")
### Workflow Workflow_a7bf5 Script
from flowix import Workflow
Workflow_a7bf5 = Workflow(Workflow_71829, "a7bf5", "Workflow_a7bf5")
## nodes
# Node StartNode_a9354 Script
from flowix import StartNode
StartNode_a9354 = StartNode(Workflow_a7bf5, "a9354", "StartNode_a9354")
# parameters
StartNode_a9354.parameters.payload = {}
# Node ScriptNode_eb289 Script
from flowix import ScriptNode
ScriptNode_eb289 = ScriptNode(Workflow_a7bf5, "eb289", "ScriptNode_eb289")
# parameters
ScriptNode_eb289.parameters.script = """
message.payload["num"] += 1

return message
"""
# Node IfNode_f819a Script
from flowix import IfNode
IfNode_f819a = IfNode(Workflow_a7bf5, "f819a", "IfNode_f819a")
# parameters
IfNode_f819a.parameters.source = """num"""
IfNode_f819a.parameters.separator = """>="""
IfNode_f819a.parameters.target = 2
# Node BreakNode_784aa Script
from flowix import BreakNode
BreakNode_784aa = BreakNode(Workflow_a7bf5, "784aa", "BreakNode_784aa")
# Node DebugNode_72cd4 Script
from flowix import DebugNode
DebugNode_72cd4 = DebugNode(Workflow_a7bf5, "72cd4", "DebugNode_72cd4")
# parameters
DebugNode_72cd4.parameters.object = """message.payload"""
DebugNode_72cd4.parameters.indent = 4
## connections
StartNode_a9354.outputs["output"].connect(ScriptNode_eb289.inputs["input"])
ScriptNode_eb289.outputs["output"].connect(IfNode_f819a.inputs["input"])
IfNode_f819a.outputs["output1"].connect(BreakNode_784aa.inputs["input"])
IfNode_f819a.outputs["output2"].connect(DebugNode_72cd4.inputs["input"])

# Node DebugNode_53203 Script
from flowix import DebugNode
DebugNode_53203 = DebugNode(Workflow_71829, "53203", "DebugNode_53203")
# parameters
DebugNode_53203.parameters.object = """message.payload"""
DebugNode_53203.parameters.indent = 4
## connections
StartNode_6f827.outputs["output"].connect(WhileNode_c7d06.inputs["input"])
WhileNode_c7d06.outputs["output"].connect(Workflow_a7bf5.inputs["input"])
Workflow_a7bf5.outputs["output"].connect(DebugNode_53203.inputs["input"])



if __name__ == "__main__":
    Workspace_ec02c4f7838544e690408e427d8244fe.execute("all")
