# -*- coding: utf-8 -*-
import os, sqlite3, uuid, pathlib, pandas as pd, copy, pickle, codecs
from typing import Any, Literal
from .workflow_message import WorkflowMessage
from .workflow_connection import WorkflowConnection
from .workflow_history import WorkflowHistory
from .node import Node, NodeInput, NodeOutput
from .nodes.start_node import StartNode


class Workflow:
    def __init__(self, workspace = None, workflow_id:str = None, workflow_name:str = None):
        if isinstance(workspace, Workflow):
            self.__workflow = workspace
            self.__workspace = None
        else:
            self.__workspace = workspace
            self.__workflow = None

        self.__workflow_id = workflow_id or self.__create_id()
        self.__workflow_name = workflow_name or f"{self.__class__.__name__}_{self.__workflow_id}"
        self.__nodes:list[Node] = []
        self.__history = WorkflowHistory(self)

        self.__state = "idle"
        self.__inputs = { "input": NodeInput(self, "input") }
        self.__outputs = { "output": NodeOutput(self, "output") }

        if self.__workspace is not None:
            self.__workspace.append_workflow(self)
            
        if self.__workflow is not None:
            self.__workflow.append_node(self)

    def __create_id(self) -> str:
        wid = uuid.uuid4().hex[:5]
        # check duplicated
        if self.__workspace is not None:
            if wid in self.__workspace.workflows.keys():
                return self.__create_id()
        elif self.__workflow is not None:
            if wid in self.__workflow.nodes.keys():
                return self.__create_id()
        
        return wid

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} id:{self.id} name:{self.name}>"
        
    @property
    def id(self) -> str:
        return self.__workflow_id

    @id.setter
    def id(self, new_id:str):
        self.__workflow_id = new_id
    
    @property
    def name(self) -> str:
        return self.__workflow_name
    
    @name.setter
    def name(self, new_name:str):
        self.__workflow_name = new_name

    @property
    def nodes(self) -> dict[str, Node]:
        return {
            node.id: node
            for node in self.__nodes
        }
        
    @property
    def connections(self) -> WorkflowConnection:
        # return empty if has no Nodes
        if len(self.__nodes) == 0:
            return WorkflowConnection(self, [])
        
        try:
            # find StartNode
            start_node:Node = [
                node
                for node in self.__nodes
                if isinstance(node, StartNode)
            ][0]
        except IndexError:
            # if no, use first appended Node
            start_node = self.__nodes[0]

        return WorkflowConnection(self, self.__get_connections(start_node))
        
    @property
    def history(self) -> WorkflowHistory:
        return self.__history

    @property
    def state(self) -> Literal["idle", "execute"]:
        return self.__state
    
    @property
    def inputs(self) -> dict[str, NodeInput]:
        return self.__inputs
    
    @property
    def outputs(self) -> dict[str, NodeOutput]:
        return self.__outputs
        
    def __get_connections(self, node:Node) -> list[dict[str, Any]]:
        node_connections = []
        for node_output in node.outputs.values():
            for node_input in node_output.connections:
                node_connections.append({
                    "from": {
                        "node": {
                            "id": node.id,
                            "name": node.name
                        },
                        "name": node_output.name
                    },
                    "to": {
                        "node": {
                            "id": node_input.node.id,
                            "name": node_input.node.name
                        },
                        "name": node_input.name
                    }
                })
                
                node_connections.extend(self.__get_connections(node_input.node))

        return node_connections

    
    def append_node(self, node:Node) -> bool:
        try:
            if not node in self.__nodes:
                # append to node list if not duplicated
                self.__nodes.append(node)
                
            return True
        except:
            return False
            
    def remove_node(self, node:Node | str) -> bool:
        try:
            if isinstance(node, Node):
                # if argument is Node, remove from list
                self.__nodes.remove(node)
            elif isinstance(node, str):
                # if argument is node_id, change node list
                self.__nodes = [
                    node_item
                    for node_item in self.__nodes
                    if node_item.id != node
                ]

            return True
        except:
            return False
        
    def execute_single_node(self, exec_id:str, message:WorkflowMessage, node:Node, previous_node:Node = None, node_output_name:str = None, nested:bool = False) -> WorkflowMessage:
        try:
            if isinstance(node, StartNode):
                history_type = "start"
            else:
                history_type = "normal"

            if previous_node is None or node_output_name is None:
                if nested:
                    history_message = f"Starting Compute {node.name}({self.name})"
                else:
                    history_message = f"Starting Compute {node.name}"
            else:
                if nested:
                    if previous_node in self.__nodes:
                        history_message = f"Starting Compute {node.name}({self.name}) from {previous_node.name}({self.name})"
                    else:
                        history_message = f"Starting Compute {node.name}({self.name}) from {previous_node.name}"
                else:
                    history_message = f"Starting Compute {node.name} from {previous_node.name}"

            self.history.add(
                exec_id, node.id,
                history_message,
                history_type
            )

            if isinstance(node, Workflow):
                message = node.execute(message, True)
                self.history.extend(node.history)
            else:
                message = node.compute(message)

            self.history.add(
                exec_id, node.id,
                "Finished" + history_message[8:],
                "normal"
            )
        except Exception as e:
            self.history.add(exec_id, node.id, str(e), "error")
            if self.__workspace is None:
                raise RuntimeError(f"Error in {node.name}\n{e}")

        if isinstance(node, Node) and not node.has_iter:
            for output_name, node_output in node.outputs.items():
                if node_output.enabled:
                    for node_input in node_output.connections:
                        next_node = node_input.node
                        if isinstance(next_node, Workflow):
                            message = next_node.execute(message)
                            self.history.extend(next_node.history)
                        else:
                            message = self.execute_single_node(exec_id, message, node_input.node, node, output_name)

        return message

    def execute(self, message:WorkflowMessage = None, nested:bool = False) -> WorkflowMessage:
        # find StartNode
        try:
            start_node:Node = [
                node
                for node in self.__nodes
                if isinstance(node, StartNode)
            ][0]
        except IndexError:
            raise RuntimeError("StartNode is required when executing Workflow!")

        if message is None:
            # create workflow message
            message = WorkflowMessage.new(uuid.uuid1().hex)

        message.nested_state = nested

        # execute start_node
        self.__state = "execute"
        message = self.execute_single_node(message.id, message, start_node, nested = nested)

        if not nested:
            # add finish history if main workflow
            self.history.add(
                message.id, None,
                "Workflow Execution Finished",
                "finish"
            )
        
        # save history to db
        if self.__workspace is not None and self.__workspace.config_db is not None:
            self.history.save(self.id, self.__workspace.config_db)

        self.__state = "idle"

        return message
        
    def save(self, workspace_config_db:sqlite3.Connection, save_history:bool = False, auto_close:bool = True):
        pd.DataFrame([[ self.id, self.serialize() ]], columns = [ "ID", "DUMPS" ]).to_sql("workflows", workspace_config_db, index = False, if_exists = "append")
        if save_history:
            self.history.save(self.id, workspace_config_db, auto_close)

        workspace_config_db.commit()
        
        if auto_close:
            workspace_config_db.close()
            
    def copy(self) -> "Workflow":
        return copy.deepcopy(self)
    
    def get_graph_info(self, nested:bool = False) -> tuple[list, list]:
        # fint startnode and other nodes
        all_nodes = [ node for node in self.__nodes ]
        try:
            start_node:Node = [
                node
                for node in all_nodes
                if isinstance(node, StartNode)
            ][0]
        except IndexError:
            start_node = all_nodes[0]

        all_nodes.remove(start_node)

        node_list, edge_list = [], []
        if nested:
            edge_list.append(( self.name, f"{start_node.name}({self.name})" ))
        
        for node in [ start_node ] + [ node for node in all_nodes ]:
            if isinstance(node, Node):
                node_list.append(f"{node.name}({self.name})" if nested else node.name)
                for node_output in node.outputs.values():
                    for node_input in node_output.connections:
                        if nested:
                            edge_list.append(( f"{node.name}({self.name})", f"{node_input.node.name}({self.name})" ))
                        else:
                            edge_list.append(( node.name, node_input.node.name ))
            elif isinstance(node, Workflow):
                nf_nodes, nf_edges = node.get_graph_info(True)
                node_list.extend(nf_nodes)
                edge_list.extend(nf_edges)
                
        if nested:
            for node_output in self.outputs.values():
                for node_input in node_output.connections:
                    edge_list.append(( node_list[-1], node_input.node.name ))

        return node_list, list(set(edge_list))
            
    def draw(self):
        import networkx as nx
        from asciinet import graph_to_ascii

        graph = nx.DiGraph()

        # fint startnode and other nodes
        all_nodes = [ node for node in self.__nodes ]
        try:
            start_node:Node = [
                node
                for node in all_nodes
                if isinstance(node, StartNode)
            ][0]
        except IndexError:
            start_node = all_nodes[0]

        all_nodes.remove(start_node)
        
        # get graph info
        node_list, edge_list = self.get_graph_info(False)
        # add nodes to graph
        graph.add_nodes_from(node_list)
        # add edges to graph
        graph.add_edges_from(edge_list)

        print(graph_to_ascii(graph))

    def to_script(self, import_string:str = None) -> str:
        if self.__workspace is None and self.__workflow is None:
            workflow_string = f'{self.name} = {self.__class__.__name__}(None, "{self.id}", "{self.name}")'
        elif self.__workspace is not None:
            workflow_string = f'{self.name} = {self.__class__.__name__}({self.__workspace.name}, "{self.id}", "{self.name}")'
        elif self.__workflow is not None:
            workflow_string = f'{self.name} = {self.__class__.__name__}({self.__workflow.name}, "{self.id}", "{self.name}")'

        if len(self.__nodes) > 0:
            workflow_string += "\n## nodes\n"
            for node in self.nodes.values():
                workflow_string += f"{node.to_script()}"

        if len(self.connections) > 0:
            workflow_string += "## connections"
            for connection in self.connections:
                workflow_string += f'\n{connection["from"]["node"]["name"]}.outputs["{connection["from"]["name"]}"].connect({connection["to"]["node"]["name"]}.inputs["{connection["to"]["name"]}"])'

        if import_string is None:
            return f"### Workflow {self.name} Script\nfrom flowix import Workflow\n" + workflow_string + "\n\n"
        else:
            return f"### Workflow {self.name} Script\n{import_string}\n" + workflow_string + "\n\n"

    # backup/restore from pickle file
    def backup_to_file(self, backup_file:str) -> bool:
        try:
            if not isinstance(backup_file, pathlib.Path):
                backup_file = pathlib.Path(backup_file).resolve()
            
            with open(str(backup_file), "wb") as bfw:
                pickle.dump(self, bfw)
            
            return True
        except:
            return False
        
    @staticmethod
    def restore_from_file(backup_file:str, remove_file:bool = False) -> "Workflow":
        backup_file = pathlib.Path(backup_file).resolve()
        if not backup_file.exists():
            raise FileNotFoundError("backup file not exists!")

        with open(backup_file, "rb") as bfr:
            workflow = pickle.load(bfr)

        if remove_file:
            os.remove(backup_file)

        return workflow
    
    def backup_to_workspace(self) -> bool:
        if self.__workspace is None:
            return False

        try:
            if self.__workspace.config_db.execute(f"select count(*) from `backups` where `ID`='{self.id}'").fetchone()[0] == 0:
                self.__workspace.config_db.execute(f"insert into `backups` values ( '{self.id}', '{self.serialize()}' );")
            else:
                self.__workspace.config_db.execute(f"update `backups` set `DUMPS`='{self.serialize}' where `ID`='{self.id}';")
                
            return True
        except:
            return False

    @staticmethod
    def restore_from_workspace(workspace, workflow_id:str) -> "Workflow":
        if workspace.config_db.execute(f"select count(*) from `backups` where `ID`='{workflow_id}';").fetchone()[0] == 0:
            raise KeyError("invalid backup id!")
        else:
            return Workflow.deserialize(workspace.config_db.execute(f"select `DUMPS` from `backups` where `ID`='{workflow_id}';").fetchone()[0])

    # serialize/deserialize from codecs string
    def serialize(self) -> str:
        return codecs.encode(pickle.dumps(self), "base64").decode()
        
    @staticmethod
    def deserialize(source:str) -> "Workflow":
        return pickle.loads(codecs.decode(source.encode(), "base64"))

    def info(self) -> dict:
        return {
            "id": self.__workflow_id,
            "name": self.__workflow_name,
            "nodes": [
                node.info()
                for node in self.__nodes
            ],
            "connections": self.connections
        }
