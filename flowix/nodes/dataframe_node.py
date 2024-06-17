# -*- coding: utf-8 -*-
import os
from ..node import Node
from ..workflow_message import WorkflowMessage


class DataframeNode(Node):
    """
    Node to convert datas from source
    """
    def __init__(self, workflow, node_id:str = None, node_name:str = None):
        """
        Parameters
        - variable_name: key used to save results in message.payload(default: df)
        - module: module to use(pandas, modin / default: pandas)
        - mode: mode for creation(data, file, sql / default: data)
        - for `data` mode
            - columns: columns argument(same as columns for pandas.DataFrame / default: [])
            - datas: data argument(same as data for pandas.DataFrame / default: [])
        - for `file` mode
            - file_type: type of source(csv, excel, json / default: csv)
            - source: path of source(file_path, url ...)
            - attrs: additional arguments(default: {})
        - for `sql` mode
            - engine: name of SQLAlchemy Engine from message.payload
            - query: query to execute
        """
        super().__init__(workflow, node_id, node_name, [ "input" ], [ "output" ], {
            "variable_name": "df",
            "module": "pandas",
            "mode": "data",
            "columns": [], "datas": [],
            "file_type": "csv", "source": None, "attrs": {},
            "engine": None, "query": None
        })
        
    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        var_name = self.parameters["variable_name"]
        if self.parameters["module"] == "modin":
            import modin.pandas as pd
        else:
            import pandas as pd
        
        if self.parameters["mode"] == "data":
            message.payload[var_name] = pd.DataFrame(self.parameters["data"], self.parameters["columns"])
        elif self.parameters["mode"] == "file":
            if self.parameters["source"] is None:
                raise ValueError("`source` must be specified!")

            file_type = self.parameters["file_type"]
            source = self.parameters["source"]
            if not file_type == "json" and not os.path.exists(source):
                raise FileNotFoundError("invalid source path!")

            attrs:dict = self.parameters["attrs"]
            if file_type == "csv":
                message.payload[var_name] = pd.read_csv(source, engine = attrs.pop("engine", "python"), encoding = attrs.pop("encoding", "utf-8"), **attrs)
            elif file_type == "excel":
                message.payload[var_name] = pd.read_excel(source, engine = attrs.pop("engine", None), sheet_name = attrs.pop("sheet_name", 0), **attrs)
            elif file_type == "json":
                message.payload[var_name] = pd.read_json(source, encoding = attrs.pop("encoding", "utf-8"), **attrs)
        if self.parameters["mode"] == "sql":
            engine_name = self.parameters["engine"]
            if not engine_name in message.payload.keys():
                raise KeyError("invalid engine name!")

            query = self.parameters["query"]
            if query is None:
                raise ValueError("`query` must be spcified!")
            
            message.payload[var_name] = pd.read_sql(query, message.payload[engine_name])
        
        return message
