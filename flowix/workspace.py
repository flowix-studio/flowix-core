# -*- coding: utf-8 -*-
import os, sqlite3, shutil, uuid, pathlib, sqlite3, pandas as pd
from .workflow import Workflow


class Workspace:
    def __init__(self, workspace_id:str = None, workspace_name:str = None, config_db_file:str = None):
        self.__workspace_id = uuid.uuid4().hex if workspace_id is None else workspace_id
        self.__workspace_name = f"{self.__class__.__name__}_{self.__workspace_id}" if workspace_name is None else workspace_name
        self.__config_db_file = config_db_file
        
        self.__workflows:list[Workflow] = []
        
    def __str__(self) -> str:
        return f"<{self.__class__.__name__} id:{self.id} name:{self.name}>"
        
    @property
    def id(self) -> str:
        return self.__workspace_id
    
    @property
    def name(self) -> str:
        return self.__workspace_name
    
    @property
    def config_db(self) -> None | sqlite3.Connection:
        if self.__config_db_file is None:
            return None
        else:
            return sqlite3.connect(self.__config_db_file)
    
    @property
    def workflows(self) -> dict[str, Workflow]:
        return {
            workflow.id: workflow
            for workflow in self.__workflows
        }
        
        
    @staticmethod
    def create(workspace_path:str, workspace_id:str = None, workspace_name:str = None) -> "Workspace":
        workspace_path:pathlib.Path = pathlib.Path(workspace_path).resolve()
        workspace_id = uuid.uuid4().hex if workspace_id is None else workspace_id

        if workspace_path.exists():
            # raise error if directory already exists
            raise FileExistsError("Cannot create Workspace into existing directory!")
        
        # create directory
        os.makedirs(str(workspace_path))
        os.makedirs(str(workspace_path.joinpath("backups")))
        
        # create config.db
        config_db_file = str(workspace_path.joinpath("flowix.config"))
        con = sqlite3.connect(config_db_file)
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
""")

        # create instance first
        workspace = Workspace(workspace_id, workspace_name, config_db_file)
        
        # save id, name into config table
        con.execute(f"insert into `config` values ('ID', '{workspace_id}'), ('NAME', '{workspace.name}');")
        con.commit()
        # close connection
        con.close()
        
        return workspace
    
    @staticmethod
    def load(workspace_path:str) -> "Workspace":
        workspace_path:pathlib.Path = pathlib.Path(workspace_path).resolve()

        # check config file exists
        config_db_file = workspace_path.joinpath("flowix.config")
        if not config_db_file.exists():
            raise FileNotFoundError("Cannot load from non-flowix format directory!")

        # connect to sqlite db
        con = sqlite3.connect(config_db_file)
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
        workspace = Workspace(configs["ID"], configs["NAME"], config_db_file)
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
    
    def save(self, workspace_path:str):
        workspace_path:pathlib.Path = pathlib.Path(workspace_path).resolve()

        # check config file exists
        config_db_file = workspace_path.joinpath("flowix.config")
        if not config_db_file.exists():
            raise FileNotFoundError("Cannot load from non-flowix format directory!")
        
        ## replace datas
        con = sqlite3.connect(config_db_file)
        # config
        con.executescript(f"""
delete from `config`;
insert into `config` values ('ID', '{self.id}'), ('NAME', '{self.name}');
""")
        # workflows/histories
        con.execute("delete from `workflows`;")
        con.execute("delete from `histories`;")
        for workflow in self.__workflows:
            workflow.save(con, True, False)

        con.commit()
        # close connection
        con.close()

        # clear backup files
        for backup_file in workspace_path.joinpath("backups").glob("*"):
            if os.path.isfile(str(backup_file)):
                os.remove(str(backup_file))
            else:
                shutil.rmtree(str(backup_file))

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
