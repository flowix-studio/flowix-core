# -*- coding: utf-8 -*-
from flowix import (
    Workspace, Workflow,
    StartNode,
    IfNode, ForNode, WhileNode, BreakNode,
    ExecNode, DataframeNode, DatabaseNode, ScriptNode, DebugNode
)


if __name__ == "__main__":
    workspace = Workspace()
    
    ## main workflow
    workflow = Workflow(workspace)
    # start node
    start_node = StartNode(workflow)
    start_node.parameters["payload"] = { "num": 0 }
    # while node
    while_node = WhileNode(workflow)
    
    ## nested workflow
    nested_workflow = Workflow(workflow)
    # start_node
    start_node_nf = StartNode(nested_workflow)
    # script node(while)
    script_node = ScriptNode(nested_workflow)
    script_node.parameters["script"] = """
message.payload["num"] += 1
print(message.payload)

return message
"""
    # if node
    if_node = IfNode(nested_workflow)
    if_node.parameters["source"] = "num"
    if_node.parameters["separator"] = ">="
    if_node.parameters["target"] = 2
    # break node
    break_node = BreakNode(nested_workflow)
    # debug node
    debug_node_nf = DebugNode(nested_workflow)
    # connect nodes(nested workflow)
    start_node_nf.outputs["output"].connect(script_node.inputs["input"])
    script_node.outputs["output"].connect(if_node.inputs["input"])
    if_node.outputs["output1"].connect(break_node.inputs["input"])
    if_node.outputs["output2"].connect(debug_node_nf.inputs["input"])

    # debug node
    debug_node = DebugNode(workflow)
    
    # connect nodes(main workflow)
    start_node.outputs["output"].connect(while_node.inputs["input"])
    while_node.outputs["output"].connect(nested_workflow.inputs["input"])
    nested_workflow.outputs["output"].connect(debug_node.inputs["input"])
    
    # check current connections
    workflow.draw()
    # looks maybe as below
    """
                 ┌───────────────┐                  
                 │StartNode_64304│                  
                 └───────┬───────┘                  
                         │                          
                         v                          
                 ┌───────────────┐                  
                 │WhileNode_2ab23│                  
                 └────────┬──────┘                  
                          │                         
                          v                         
                  ┌──────────────┐                  
                  │Workflow_41e5e│                  
                  └──────┬───────┘                  
                         │                          
                         v                          
         ┌───────────────────────────────┐          
         │StartNode_1c5ac(Workflow_41e5e)│          
         └────────────────┬──────────────┘          
                          │                         
                          v                         
         ┌────────────────────────────────┐         
         │ScriptNode_dba4d(Workflow_41e5e)│         
         └────────────────┬───────────────┘         
                          │                         
                          v                         
           ┌────────────────────────────┐           
           │IfNode_aa31d(Workflow_41e5e)│           
           └─────────┬─────────┬────────┘           
                     │         │                    
                     │         └───────────┐        
                     v                     │        
     ┌───────────────────────────────┐     │        
     │DebugNode_e4e39(Workflow_41e5e)│     │        
     └───┬───────────────────────────┘     │        
         │                                 │        
         v                                 v        
 ┌───────────────┐ ┌───────────────────────────────┐
 │DebugNode_109f4│ │BreakNode_cf9d0(Workflow_41e5e)│
 └───────────────┘ └───────────────────────────────┘
    """

    # execute workflow
    workflow.execute()

    # print history
    workflow.history.pprint()
    # looks maybe as below
    """
[History of Workflow(82cd2)]
[
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "27e31",
        "TYPE": "start",
        "MESSAGE": "Starting Compute StartNode_27e31"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "27e31",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute StartNode_27e31"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "35020",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute WhileNode_35020 from StartNode_27e31"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "39086",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute Workflow_39086"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "4a120",
        "TYPE": "start",
        "MESSAGE": "Starting Compute StartNode_4a120(Workflow_39086)"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "4a120",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute StartNode_4a120(Workflow_39086)"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "6c9d1",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute ScriptNode_6c9d1 from StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "6c9d1",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute ScriptNode_6c9d1 from StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "a09bf",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute IfNode_a09bf from ScriptNode_6c9d1"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "a09bf",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute IfNode_a09bf from ScriptNode_6c9d1"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "934f1",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute DebugNode_934f1 from IfNode_a09bf"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "934f1",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute DebugNode_934f1 from IfNode_a09bf"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "39086",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute Workflow_39086"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "39086",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute Workflow_39086"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "4a120",
        "TYPE": "start",
        "MESSAGE": "Starting Compute StartNode_4a120(Workflow_39086)"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "4a120",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute StartNode_4a120(Workflow_39086)"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "6c9d1",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute ScriptNode_6c9d1 from StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "6c9d1",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute ScriptNode_6c9d1 from StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "a09bf",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute IfNode_a09bf from ScriptNode_6c9d1"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "a09bf",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute IfNode_a09bf from ScriptNode_6c9d1"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "934f1",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute DebugNode_934f1 from IfNode_a09bf"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "934f1",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute DebugNode_934f1 from IfNode_a09bf"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "4a120",
        "TYPE": "start",
        "MESSAGE": "Starting Compute StartNode_4a120(Workflow_39086)"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "4a120",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute StartNode_4a120(Workflow_39086)"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "6c9d1",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute ScriptNode_6c9d1 from StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "6c9d1",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute ScriptNode_6c9d1 from StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "a09bf",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute IfNode_a09bf from ScriptNode_6c9d1"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "a09bf",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute IfNode_a09bf from ScriptNode_6c9d1"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "59700",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute BreakNode_59700 from IfNode_a09bf"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "59700",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute BreakNode_59700 from IfNode_a09bf"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "39086",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute Workflow_39086"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "35020",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute WhileNode_35020 from StartNode_27e31"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "4a120",
        "TYPE": "start",
        "MESSAGE": "Starting Compute StartNode_4a120(Workflow_39086)"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "4a120",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute StartNode_4a120(Workflow_39086)"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "6c9d1",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute ScriptNode_6c9d1 from StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "6c9d1",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute ScriptNode_6c9d1 from StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "a09bf",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute IfNode_a09bf from ScriptNode_6c9d1"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "a09bf",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute IfNode_a09bf from ScriptNode_6c9d1"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "934f1",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute DebugNode_934f1 from IfNode_a09bf"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "934f1",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute DebugNode_934f1 from IfNode_a09bf"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "4a120",
        "TYPE": "start",
        "MESSAGE": "Starting Compute StartNode_4a120(Workflow_39086)"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "4a120",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute StartNode_4a120(Workflow_39086)"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "6c9d1",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute ScriptNode_6c9d1 from StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "6c9d1",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute ScriptNode_6c9d1 from StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "a09bf",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute IfNode_a09bf from ScriptNode_6c9d1"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "a09bf",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute IfNode_a09bf from ScriptNode_6c9d1"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "59700",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute BreakNode_59700 from IfNode_a09bf"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "59700",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute BreakNode_59700 from IfNode_a09bf"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "4a120",
        "TYPE": "start",
        "MESSAGE": "Starting Compute StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "4a120",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "6c9d1",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute ScriptNode_6c9d1 from StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "6c9d1",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute ScriptNode_6c9d1 from StartNode_4a120"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "a09bf",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute IfNode_a09bf from ScriptNode_6c9d1"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "a09bf",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute IfNode_a09bf from ScriptNode_6c9d1"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "59700",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute BreakNode_59700 from IfNode_a09bf"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "NODE_ID": "59700",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute BreakNode_59700 from IfNode_a09bf"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "TYPE": "finish",
        "MESSAGE": "Workflow Execution Finished"
    },
    {
        "EXEC_ID": "acd289742cab11ef8a9a7277b40fc923",
        "TYPE": "finish",
        "MESSAGE": "Workflow Execution Finished"
    }
]
"""
