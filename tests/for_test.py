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

    # dataframe node
    dataframe_node = DataframeNode(workflow)
    dataframe_node.parameters.mode = "file"
    dataframe_node.parameters.file_type = "json"
    dataframe_node.parameters.source = "https://jsonplaceholder.typicode.com/posts"

    # for node
    for_node = ForNode(workflow)
    for_node.parameters.max_iter = 2
    for_node.parameters.mode = "payload"
    for_node.parameters.source = "df"
    # debug node
    debug_node = DebugNode(workflow)
    debug_node.parameters.object = "message.payload['for_iter']"
    
    # connect nodes
    start_node.outputs["output"].connect(dataframe_node.inputs["input"])
    dataframe_node.outputs["output"].connect(for_node.inputs["input"])
    for_node.outputs["output"].connect(debug_node.inputs["input"])
    
    # check current connections
    workflow.draw()
    # looks maybe as below
    """
  ┌───────────────┐   
  │StartNode_3da4d│   
  └────────┬──────┘   
           │          
           v          
 ┌───────────────────┐
 │DataframeNode_d3bd0│
 └────────┬──────────┘
          │           
          v           
   ┌─────────────┐    
   │ForNode_112a9│    
   └──────┬──────┘    
          │           
          v           
  ┌───────────────┐   
  │DebugNode_ac866│   
  └───────────────┘
"""

    # execute workflow
    workflow.execute()
    # looks maybe as below
    """
{
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
{
    "userId": 1,
    "id": 2,
    "title": "qui est esse",
    "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"
}
{
    "userId": 1,
    "id": 2,
    "title": "qui est esse",
    "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"
}
"""

    # print history
    workflow.history.pprint()
    # looks maybe as below
    """
[History of Workflow(c8293)]
[
    {
        "EXEC_ID": "a87c933a2cae11efbe6c7277b40fc923",
        "NODE_ID": "4ddd3",
        "TYPE": "start",
        "MESSAGE": "Starting Compute StartNode_4ddd3"
    },
    {
        "EXEC_ID": "a87c933a2cae11efbe6c7277b40fc923",
        "NODE_ID": "4ddd3",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute StartNode_4ddd3"
    },
    {
        "EXEC_ID": "a87c933a2cae11efbe6c7277b40fc923",
        "NODE_ID": "f1efe",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute DataframeNode_f1efe from StartNode_4ddd3"
    },
    {
        "EXEC_ID": "a87c933a2cae11efbe6c7277b40fc923",
        "NODE_ID": "f1efe",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute DataframeNode_f1efe from StartNode_4ddd3"
    },
    {
        "EXEC_ID": "a87c933a2cae11efbe6c7277b40fc923",
        "NODE_ID": "a0109",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute ForNode_a0109 from DataframeNode_f1efe"
    },
    {
        "EXEC_ID": "a87c933a2cae11efbe6c7277b40fc923",
        "NODE_ID": "ca307",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute DebugNode_ca307"
    },
    {
        "EXEC_ID": "a87c933a2cae11efbe6c7277b40fc923",
        "NODE_ID": "ca307",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute DebugNode_ca307"
    },
    {
        "EXEC_ID": "a87c933a2cae11efbe6c7277b40fc923",
        "NODE_ID": "ca307",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute DebugNode_ca307"
    },
    {
        "EXEC_ID": "a87c933a2cae11efbe6c7277b40fc923",
        "NODE_ID": "ca307",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute DebugNode_ca307"
    },
    {
        "EXEC_ID": "a87c933a2cae11efbe6c7277b40fc923",
        "NODE_ID": "a0109",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute ForNode_a0109 from DataframeNode_f1efe"
    },
    {
        "EXEC_ID": "a87c933a2cae11efbe6c7277b40fc923",
        "NODE_ID": "ca307",
        "TYPE": "normal",
        "MESSAGE": "Starting Compute DebugNode_ca307 from ForNode_a0109"
    },
    {
        "EXEC_ID": "a87c933a2cae11efbe6c7277b40fc923",
        "NODE_ID": "ca307",
        "TYPE": "normal",
        "MESSAGE": "Finished Compute DebugNode_ca307 from ForNode_a0109"
    },
    {
        "EXEC_ID": "a87c933a2cae11efbe6c7277b40fc923",
        "TYPE": "finish",
        "MESSAGE": "Workflow Execution Finished"
    }
]
"""
