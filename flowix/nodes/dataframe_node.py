# -*- coding: utf-8 -*-
import os
from typing import Literal
from ..node import Node, NodeParameters
from ..workflow_message import WorkflowMessage


class DataframeNodeParameters(NodeParameters):
    """
    Parameters
    - variable_name: key used to save results in message.payload(default: df)
    - module: module to use(pandas, modin / default: pandas)
    - mode: mode for creation(data, file, sql / default: data)
    - for `data` mode
        - columns: columns argument(same as columns for pandas.DataFrame / default: [])
        - data: data argument(same as data for pandas.DataFrame / default: [])
    - for `file` mode
        - file_type: type of source(csv, excel, json / default: csv)
        - source: path of source(file_path, url ...)
        - attrs: additional arguments(default: {})
    - for `sql` mode
        - engine: name of SQLAlchemy Engine from message.payload
        - query: query to execute
    """
    variable_name:str
    module:Literal["pandas", "modin"]
    mode:Literal["data", "file", "sql"]
    # for data
    columns:list
    data:list
    # for file
    file_type:Literal["csv", "excel", "json"]
    source:str
    attrs:dict
    # for sql
    engine:str
    query:str

class DataframeNode(Node):
    """
    Node to convert datas from source
    """
    def __init__(self, workflow, node_id:str = None, node_name:str = None):
        super().__init__(workflow, node_id, node_name, [ "input" ], [ "output" ], {
            "variable_name": { "type": str, "default": "df"},
            "module": { "type": str, "default": "pandas"},
            "mode": { "type": str, "default": "data"},
            "columns": { "type": list, "default": [] }, "data": { "type": list, "default": [] },
            "file_type": { "type": str, "default": "csv"}, "source": str, "attrs": { "type": dict, "default": {} },
            "engine": str, "query": str
        })

    @property
    def parameters(self) -> DataframeNodeParameters:
        return super().parameters

        
    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        var_name = self.parameters.variable_name
        if self.parameters.module == "modin":
            import modin.pandas as pd
        else:
            import pandas as pd
        
        if self.parameters.mode == "data":
            message.payload[var_name] = pd.DataFrame(self.parameters.data, self.parameters.columns)
        elif self.parameters.mode == "file":
            if self.parameters.source is None:
                raise ValueError("`source` must be specified!")

            file_type = self.parameters.file_type
            source = self.parameters.source
            if not file_type == "json" and not os.path.exists(source):
                raise FileNotFoundError("invalid source path!")

            attrs = self.parameters.attrs
            if file_type == "csv":
                message.payload[var_name] = pd.read_csv(source, engine = attrs.pop("engine", "python"), encoding = attrs.pop("encoding", "utf-8"), **attrs)
            elif file_type == "excel":
                message.payload[var_name] = pd.read_excel(source, engine = attrs.pop("engine", None), sheet_name = attrs.pop("sheet_name", 0), **attrs)
            elif file_type == "json":
                message.payload[var_name] = pd.read_json(source, encoding = attrs.pop("encoding", "utf-8"), **attrs)
        if self.parameters.mode == "sql":
            engine_name = self.parameters.engine
            if not engine_name in message.payload.keys():
                raise KeyError("invalid engine name!")

            query = self.parameters.query
            if query is None:
                raise ValueError("`query` must be spcified!")
            
            message.payload[var_name] = pd.read_sql(query, message.payload[engine_name])
        
        return message
    
    def to_script(self) -> str:
        return super().to_script()
