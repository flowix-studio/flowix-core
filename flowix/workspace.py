# -*- coding: utf-8 -*-
import os, sqlite3, uuid, pathlib, sqlite3, pandas as pd
from .workflow import Workflow


class Workspace:
    def __init__(self, workspace_id:str = None, workspace_name:str = None, workspace_file:str = None):
        self.__workspace_id = uuid.uuid4().hex if workspace_id is None else workspace_id
        self.__workspace_name = f"{self.__class__.__name__}_{self.__workspace_id}" if workspace_name is None else workspace_name
        self.__workspace_file = workspace_file
        
        self.__workflows:list[Workflow] = []
        
    def __str__(self) -> str:
        return f"<{self.__class__.__name__} id:{self.id} name:{self.name}>"
        
    @property
    def id(self) -> str:
        return self.__workspace_id

    @id.setter
    def id(self, new_id:str):
        self.__workspace_id = new_id

    @property
    def name(self) -> str:
        return self.__workspace_name

    @name.setter
    def name(self, new_name:str):
        self.__workspace_name = new_name
    
    @property
    def config_db(self) -> None | sqlite3.Connection:
        if self.__workspace_file is None:
            return None
        else:
            return sqlite3.connect(self.__workspace_file)
    
    @property
    def workflows(self) -> dict[str, Workflow]:
        return {
            workflow.id: workflow
            for workflow in self.__workflows
        }
        
        
    @staticmethod
    def create(workspace_file:str, workspace_id:str = None, workspace_name:str = None) -> "Workspace":
        workspace_file:pathlib.Path = pathlib.Path(workspace_file).resolve()
        workspace_id = uuid.uuid4().hex if workspace_id is None else workspace_id

        if workspace_file.exists():
            # raise error if file already exists
            raise FileExistsError("File exists!")

        con = sqlite3.connect(str(workspace_file))
        # create tables
        con.executescript("""
create table `config` (
    `NAME` text primary key not null,
    `VALUE` text not null
);
create table `workflows` (
    `ID` text primary key not null,
    `DUMPS` text not null
);
create table `histories` (
    `WORKFLOW` text not null,
    `EXEC_ID` text not null,
    `NODE_ID` text,
    `TYPE` text not null,
    `MESSAGE` text not null
);
create table `backups` (
    `ID` text not null,
    `DUMPS` text not null
);
create table `guimaps` (
    `WORKFLOW` text not null,
    `NODE` text not null,
    `X` real not null,
    `Y` real not null
);
""")

        # create instance first
        workspace = Workspace(workspace_id, workspace_name, str(workspace_file))
        
        # save id, name into config table
        con.execute(f"insert into `config` values ('ID', '{workspace_id}'), ('NAME', '{workspace.name}');")
        con.commit()
        # close connection
        con.close()
        
        return workspace
    
    @staticmethod
    def load(workspace_file:str) -> "Workspace":
        workspace_file:pathlib.Path = pathlib.Path(workspace_file).resolve()

        # check file exists
        if not workspace_file.exists():
            raise FileNotFoundError("File not exists!")

        # connect to sqlite db
        con = sqlite3.connect(str(workspace_file))
        con.row_factory = sqlite3.Row
        # get config from table
        configs = {
            row[0]: row[1]
            for row in con.execute("select * from `config`;").fetchall()
        }
        # get workflows from table
        workflows = [
            row[0]
            for row in con.execute("select `DUMPS` from `workflows`").fetchall()
        ]

        # create workspace from configs
        workspace = Workspace(configs["ID"], configs["NAME"], str(workspace_file))
        # append workflows
        for workflow_dump in workflows:
            workflow = Workflow.deserialize(workflow_dump)
            # get histories
            df_history:pd.DataFrame = pd.read_sql(f"select `EXEC_ID`, `NODE_ID`, `TYPE`, `MESSAGE` from `histories` where `WORKFLOW`='{workflow.id}' order by `EXEC_ID`;", con)
            # change history list from db records
            workflow.history.clear()
            for history in df_history.to_dict(orient = "records"):
                workflow.history.append(history["EXEC_ID"], history["NODE_ID"], history["MESSAGE"], history["TYPE"])

            # append workflow
            workspace.append_workflow(workflow)

        # close connection
        con.close()

        return workspace
    
    def save(self) -> bool:
        if self.__workspace_file is None:
            return False
        
        ## replace datas
        # config
        self.config_db.executescript(f"""
delete from `config`;
insert into `config` values ('ID', '{self.id}'), ('NAME', '{self.name}');
""")
        self.config_db.commit()

        # workflows/histories
        self.config_db.executescript("""
delete from `workflows`;
delete from `histories`;
""")
        self.config_db.commit()
        for workflow in self.__workflows:
            workflow.save(self.config_db, True, False)

        self.config_db.commit()
        # close connection
        self.config_db.close()
        
    def save_as(self, workspace_file:str, overwrite:bool = False) -> bool:
        workspace_file:pathlib.Path = pathlib.Path(workspace_file).resolve()
        if not overwrite and workspace_file.exists():
            return False
        
        if overwrite and workspace_file.exists():
            os.remove(str(workspace_file))
        
        con = sqlite3.connect(str(workspace_file))
        # create tables
        con.executescript("""
create table `config` (
    `NAME` text primary key not null,
    `VALUE` text not null
);
create table `workflows` (
    `ID` text primary key not null,
    `DUMPS` text not null
);
create table `histories` (
    `WORKFLOW` text not null,
    `EXEC_ID` text not null,
    `NODE_ID` text,
    `TYPE` text not null,
    `MESSAGE` text not null
);
create table `backups` (
    `ID` text not null,
    `DUMPS` text not null
);
create table `guimaps` (
    `WORKFLOW` text not null,
    `NODE` text not null,
    `X` real not null,
    `Y` real not null
);
""")

        ## insert datas
        # config
        con.execute(f"""
insert into `config` values ('ID', '{self.id}'), ('NAME', '{self.name}');
""")
        # workflows/histories
        for workflow in self.__workflows:
            workflow.save(con, True, False)

        con.commit()
        # close connection
        con.close()

    def append_workflow(self, workflow:Workflow) -> bool:
        try:
            if not workflow in self.__workflows:
                self.__workflows.append(workflow)

            return True
        except:
            return False
        
    def remove_workflow(self, workflow:str | Workflow) -> bool:
        try:
            if isinstance(workflow, Workflow):
                self.__workflows.pop(workflow)
            else:
                self.__workflows = {
                    key: value
                    for key, value in self.__workflows.items()
                    if key != workflow
                }
                
            return True
        except:
            return False
        
    def execute(self, workflow:str = "all"):
        if workflow == "all":
            for workflow in self.__workflows:
                workflow.execute()
        else:
            try:
                self.workflows[workflow].execute()
            except KeyError:
                raise KeyError(f"No such workflow of id({workflow})!")

    def to_script(self, import_string:str = None) -> str:
        if self.__workspace_file is None:
            workspace_string = f'{self.name} = {self.__class__.__name__}("{self.id}", "{self.name}")'
        else:
            workspace_string = f'{self.name} = {self.__class__.__name__}("{self.id}", "{self.name}", "{self.__workspace_file}")'

        if len(self.__workflows) > 0:
            workspace_string += "\n\n#### workflows\n"
            for workflow in self.workflows.values():
                workspace_string += f"{workflow.to_script()}"
            
        if import_string is None:
            workspace_string = "from flowix import Workspace\n" + workspace_string
        else:
            workspace_string = import_string + "\n" + workspace_string
            
        return f"""# -* coding: utf-8 -*-
# Automatically Exported Script of Flowix Workspace

##### Workspace {self.name} Script
{workspace_string}

if __name__ == "__main__":
    {self.name}.execute("all")
"""

    def info(self) -> dict:
        return {
            "id": self.__workspace_id,
            "name": self.__workspace_name,
            "workflows": [
                workflow.info()
                for workflow in self.__workflows
            ]
        }
