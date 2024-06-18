# -*- coding: utf-8 -*-
from flowix import (
    Workspace, Workflow,
    StartNode,
    IfNode, ForNode, WhileNode, BreakNode,
    ExecNode, DataframeNode, DatabaseNode, ScriptNode, DebugNode
)


if __name__ == "__main__":
    workspace = Workspace()
    
    workflow = Workflow(workspace)

    # start node
    start_node = StartNode(workflow)
    start_node.parameters.payload = { "num": 0 }

    # while node
    while_node = WhileNode(workflow)
    # script node(while)
    script_node = ScriptNode(workflow)
    script_node.parameters.script = """
message.payload["num"] += 1

return message
"""
    # if node
    if_node = IfNode(workflow)
    if_node.parameters.source = "num"
    if_node.parameters.separator = ">="
    if_node.parameters.target = 2
    # break node
    break_node = BreakNode(workflow)

    # debug node
    debug_node = DebugNode(workflow)
    
    # connect nodes
    start_node.outputs["output"].connect(while_node.inputs["input"])
    while_node.outputs["output"].connect(script_node.inputs["input"])
    script_node.outputs["output"].connect(if_node.inputs["input"])
    if_node.outputs["output1"].connect(break_node.inputs["input"])
    break_node.outputs["output"].connect(debug_node.inputs["input"])
    
    # check current connections
    workflow.draw()
    # looks maybe as below
    """
 ┌───────────────┐ 
 │StartNode_94659│ 
 └───────┬───────┘ 
         │         
         v         
 ┌───────────────┐ 
 │WhileNode_b19e0│ 
 └────────┬──────┘ 
          │        
          v        
 ┌────────────────┐
 │ScriptNode_fc2f1│
 └───────┬────────┘
         │         
         v         
  ┌────────────┐   
  │IfNode_6ab06│   
  └──────┬─────┘   
         │         
         v         
 ┌───────────────┐ 
 │BreakNode_9a5f4│ 
 └───────┬───────┘ 
         │         
         v         
 ┌───────────────┐ 
 │DebugNode_bd1cc│ 
 └───────────────┘
"""

    # execute workflow
    workflow.execute()

    # print history
    workflow.history.pprint()
    # looks maybe as below
    """
[History of Workflow(cb2b3)]
[
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "ee850",
        "TYPE": "start",
        "MESSAGE": "Starting Compute StartNode_ee850"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "ee850",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute StartNode_ee850"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "84905",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute WhileNode_84905 from StartNode_ee850"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "b49cb",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute ScriptNode_b49cb"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "b49cb",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute ScriptNode_b49cb"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "d06d5",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute IfNode_d06d5 from ScriptNode_b49cb"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "d06d5",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute IfNode_d06d5 from ScriptNode_b49cb"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "b49cb",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute ScriptNode_b49cb"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "b49cb",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute ScriptNode_b49cb"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "d06d5",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute IfNode_d06d5 from ScriptNode_b49cb"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "d06d5",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute IfNode_d06d5 from ScriptNode_b49cb"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "7f0a5",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute BreakNode_7f0a5 from IfNode_d06d5"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "7f0a5",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute BreakNode_7f0a5 from IfNode_d06d5"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "bb286",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute DebugNode_bb286 from BreakNode_7f0a5"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "bb286",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute DebugNode_bb286 from BreakNode_7f0a5"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "84905",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute WhileNode_84905 from StartNode_ee850"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "b49cb",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute ScriptNode_b49cb from WhileNode_84905"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "b49cb",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute ScriptNode_b49cb from WhileNode_84905"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "d06d5",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute IfNode_d06d5 from ScriptNode_b49cb"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "d06d5",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute IfNode_d06d5 from ScriptNode_b49cb"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "7f0a5",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute BreakNode_7f0a5 from IfNode_d06d5"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "7f0a5",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute BreakNode_7f0a5 from IfNode_d06d5"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "bb286",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute DebugNode_bb286 from BreakNode_7f0a5"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "NODE_ID": "bb286",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute DebugNode_bb286 from BreakNode_7f0a5"
    },
    {
        "EXEC_ID": "f11e957a2ca911ef96d27277b40fc923",
        "TYPE": "finish",
        "MESSAGE": "Workflow Execution Finished"
    }
]
"""
