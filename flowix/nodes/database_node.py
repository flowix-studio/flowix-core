# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, URL
from urllib.parse import quote_plus
from ..node import Node
from ..workflow_message import WorkflowMessage


class DatabaseNode(Node):
    """
    Node for create SQLAlchemy Engine
    """
    def __init__(self, workflow, node_id:str = None, node_name:str = None):
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
        super().__init__(workflow, node_id, node_name, [ "input" ], [ "output" ], {
            "variable_name": "engine",
            "type": None,
            "host": None, "port": None, "user": None, "psswd": None, "database": None,
            "file": None
        })

    def compute(self, message:WorkflowMessage) -> WorkflowMessage:
        if self.parameters["type"] == "sqlite":
            engine = create_engine(f"sqlite:///{':memory:' if self.parameters['file'] is None else self.parameters['file']}")
        elif self.parameters["type"] in ( "mysql", "mariadb" ):
            if self.parameters["user"] is None or self.parameters["psswd"] is None or self.parameters["host"] is None:
                raise ValueError("`user`, `psswd`, `host` parameter cannot be empty!")
            
            engine = create_engine(URL.create(
                "mysql+pymysql",
                self.parameters['user'], quote_plus(self.parameters['psswd']),
                self.parameters['host'], 3306 if self.parameters['port'] is None else self.parameters['port'],
                self.parameters['database']
            ))
        elif self.parameters["type"] == "postgresql":
            if self.parameters["user"] is None or self.parameters["psswd"] is None or self.parameters["host"] is None:
                raise ValueError("`user`, `psswd`, `host` parameter cannot be empty!")
            
            engine = create_engine(URL.create(
                "postgresql+psycopg",
                self.parameters['user'], quote_plus(self.parameters['psswd']),
                self.parameters['host'], 5432 if self.parameters['port'] is None else self.parameters['port'],
                self.parameters['database']
            ))
        elif self.parameters["type"] == "oracle":
            if self.parameters["user"] is None or self.parameters["psswd"] is None or self.parameters["host"] is None:
                raise ValueError("`user`, `psswd`, `host` parameter cannot be empty!")
            
            engine = create_engine(URL.create(
                "oracle+oracledb",
                self.parameters['user'], quote_plus(self.parameters['psswd']),
                self.parameters['host'], 1521 if self.parameters['port'] is None else self.parameters['port'],
                self.parameters['database']
            ))
        elif self.parameters["type"] == "mssql":
            if self.parameters["user"] is None or self.parameters["psswd"] is None or self.parameters["host"] is None:
                raise ValueError("`user`, `psswd`, `host` parameter cannot be empty!")
            
            engine = create_engine(URL.create(
                "mssql+pymssql",
                self.parameters['user'], quote_plus(self.parameters['psswd']),
                self.parameters['host'], 1433 if self.parameters['port'] is None else self.parameters['port'],
                self.parameters['database']
            ))
            
        message.payload[self.parameters["variable_name"]] = engine
        
        return message
