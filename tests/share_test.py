# -*- coding: utf-8 -*-
from flowix import (
    Workflow, WorkflowMessage,
    Node, StartNode, DebugNode,
    ShareManager
)


class CustomNode(Node):
    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        message.payload["message"] = ["I'm Custom Node!"]

        return message


if __name__ == "__main__":
    manager = ShareManager("88703e00a73f4b28b65871269cdf1983")
    # connect to share server
    print("connected: ", manager.connect("127.0.0.1", 8080))

    # create workflow, nodes
    workflow = Workflow(workflow_id = "77404")
    start_node = StartNode(workflow, "6542a")
    custom_node = CustomNode(workflow, "54c94")
    debug_node = DebugNode(workflow, "0dabe")
    # make connections
    start_node.outputs["output"].connect(custom_node.inputs["input"])
    custom_node.outputs["output"].connect(debug_node.inputs["input"])

    # check workflow by draw
    workflow.draw()
    # looks maybe as below
    """
 ┌───────────────┐ 
 │StartNode_6542a│ 
 └────────┬──────┘ 
          │        
          v        
 ┌────────────────┐
 │CustomNode_54c94│
 └───────┬────────┘
         │         
         v         
 ┌───────────────┐ 
 │DebugNode_0dabe│ 
 └───────────────┘
"""

    # execute workflow for compare(original)
    workflow.execute()
    # looks maybe as below
    """
{
    "message": [
        "I'm Custom Node!"
    ]
}
"""
    
    # share workflow
    print("shared(workflow): ", manager.share(workflow))
    # share custom node
    print("shared(custom_node): ", manager.share(custom_node))
    
    # check current shared items
    print(manager.shared)
    # looks maybe as below
    """
[{'id': '77404', 'type': 'Workflow', 'object': '**********'}, {'id': '54c94', 'type': 'Node', 'object': '**********'}]
"""

    # get shared workflow
    workflow_shared:Workflow = manager.load("77404")
    # check workflow_shared by draw
    workflow_shared.draw()
    # looks maybe as below
    """
 ┌───────────────┐ 
 │StartNode_6542a│ 
 └────────┬──────┘ 
          │        
          v        
 ┌────────────────┐
 │CustomNode_54c94│
 └───────┬────────┘
         │         
         v         
 ┌───────────────┐ 
 │DebugNode_0dabe│ 
 └───────────────┘
"""
    # execute workflow_shared for compare(shared)
    workflow_shared.execute()
    # looks maybe as below
    """
{
    "message": [
        "I'm Custom Node!"
    ]
}
"""
    
    # unshare all
    print("unshared: ", manager.unshare_all())

    # disconnect from share server
    print("disconnected: ", manager.disconnect())
