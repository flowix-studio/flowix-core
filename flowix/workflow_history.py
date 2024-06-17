# -*- coding: utf-8 -*-
import sqlite3, pandas as pd, json
from typing import Literal
from collections import OrderedDict


class WorkflowHistory(list):
    def __init__(self, workflow, histories:list[dict] = []):
        super().__init__(histories)

        self.__workflow_id = workflow.id

    def add(self, exec_id:str, node_id:str, history_message:str, history_type:Literal["start", "finish", "normal", "error"]):
        history = OrderedDict()
        history["EXEC_ID"] = exec_id
        if node_id is not None:
            history["NODE_ID"] = node_id

        history["TYPE"] = history_type
        history["MESSAGE"] = history_message

        self.append(history)

    def save(self, workflow_id:str, workspace_config_db:sqlite3.Connection, auto_close:bool = True):
        if len(self) > 0:
            df_history = pd.DataFrame.from_records(self)
            df_history.insert(0, "WORKFLOW", workflow_id)
            
            df_history.to_sql("histories", workspace_config_db, index = False, if_exists = "append")

            if auto_close:
                workspace_config_db.close()
                
    def save_as(self, csv_file:str):
        if len(self) > 0:
            pd.DataFrame.from_records(self).to_csv(csv_file, index = False, encoding = "utf-8")

    def pprint(self, indent = 4):
        print(f"[History of Workflow({self.__workflow_id})]\n{json.dumps(self, indent = indent)}")
