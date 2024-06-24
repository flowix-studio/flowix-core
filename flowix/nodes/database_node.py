# -*- coding: utf-8 -*-
from typing import Literal
from sqlalchemy import create_engine, URL
from urllib.parse import quote_plus
from ..node import Node, NodeParameters
from ..workflow_message import WorkflowMessage


class DatabaseNodeParameters(NodeParameters):
    """
    Parameters
    - variable_name: key used to save results in message.payload(default: engine)
    - type: type for database(sqlite, mysql, mariadb, postgresql, oragle, mssql)
    - for `remote` databases
        - host: host of database server
        - port: port of database server
        - user: id for connecting to database server
        - psswd: password for connecting to database server
        - database: database(schema) of database server
    - for `non-remote` databases
        - file: target database file
    """
    variable_name:str
    type:Literal["sqlite", "mysql", "mariadb", "postgresql", "oracle", "mssql"]
    # for remote
    host:str
    port:int
    user:str
    psswd:str
    database:str
    # for non-remote
    file:str

class DatabaseNode(Node):
    """
    Node for create SQLAlchemy Engine
    """
    def __init__(self, workflow = None, node_id:str = None, node_name:str = None):
        super().__init__(workflow, node_id, node_name, [ "input" ], [ "output" ], {
            "variable_name": { "type": str, "default": "engine"},
            "type": str,
            "host": str, "port": int, "user": str, "psswd": str, "database": str,
            "file": str
        })
    
    @property
    def parameters(self) -> DatabaseNodeParameters:
        return super().parameters


    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        if self.parameters.type == "sqlite":
            engine = create_engine(f"sqlite:///{self.parameters.file or ':memory:'}")
        elif self.parameters.type in ( "mysql", "mariadb" ):
            if self.parameters.user is None or self.parameters.psswd is None or self.parameters.host is None:
                raise ValueError("`user`, `psswd`, `host` parameter cannot be empty!")

            engine = create_engine(URL.create(
                "mysql+pymysql",
                self.parameters.user, quote_plus(self.parameters.psswd),
                self.parameters.host, self.parameters.port or 3306,
                self.parameters.database
            ))
        elif self.parameters.type == "postgresql":
            if self.parameters.user is None or self.parameters.psswd is None or self.parameters.host is None:
                raise ValueError("`user`, `psswd`, `host` parameter cannot be empty!")

            engine = create_engine(URL.create(
                "postgresql+psycopg",
                self.parameters.user, quote_plus(self.parameters.psswd),
                self.parameters.host, self.parameters.port or 5432,
                self.parameters.database
            ))
        elif self.parameters.type == "oracle":
            if self.parameters.user is None or self.parameters.psswd is None or self.parameters.host is None:
                raise ValueError("`user`, `psswd`, `host` parameter cannot be empty!")

            engine = create_engine(URL.create(
                "oracle+oracledb",
                self.parameters.user, quote_plus(self.parameters.psswd),
                self.parameters.host, self.parameters.port or 1521,
                self.parameters.database
            ))
        elif self.parameters.type == "mssql":
            if self.parameters.user is None or self.parameters.psswd is None or self.parameters.host is None:
                raise ValueError("`user`, `psswd`, `host` parameter cannot be empty!")

            engine = create_engine(URL.create(
                "mssql+pymssql",
                self.parameters.user, quote_plus(self.parameters.psswd),
                self.parameters.host, self.parameters.port or 1433,
                self.parameters.database
            ))
        else:
            raise TypeError("invalid database type!")

        message.payload[self.parameters.variable_name] = engine
        
        return message

    def to_script(self) -> str:
        return super().to_script()
