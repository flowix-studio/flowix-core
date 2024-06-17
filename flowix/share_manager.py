# -*- coding: utf-8 -*-
import uuid, requests
from .node import Node
from .workflow import Workflow


class ShareManager:
    def __init__(self, manager_id:str):
        self.__manager_id = uuid.uuid4().hex if manager_id is None else manager_id
        self.__base_url = None
        self.__token = None
        
    @property
    def id(self) -> str:
        return self.__manager_id
    
    @property
    def shared(self) -> list[dict[str, str]]:
        if self.__base_url is None:
            return []

        try:
            result = requests.get(
                self.__base_url + f"/share/{self.id}",
                headers = { "flowix_token": self.__token }
            ).json()

            if result["state"] == "fail":
                return []

            return result["objects"]
        except:
            return []
        
    def connect(self, host:str, port:int, https:bool = False) -> bool:
        self.__base_url = base_url = f"{'https' if https else 'http'}://{host}{'' if port == 80 else f':{port}'}"

        try:
            self.__token = requests.post(base_url + "/connect").json()["token"]

            return True
        except:
            return False
        
    def disconnect(self) -> bool:
        if self.__base_url is None:
            return False

        try:
            return requests.post(
                self.__base_url + "/disconnect",
                headers = { "flowix_token": self.__token }
            ).json()["state"] == "success"
        except:
            return False
        
    def share(self, object:Node | Workflow) -> bool:
        try:
            return requests.post(
                self.__base_url + "/share",
                data = {
                    "manager": self.id,
                    "id": object.id,
                    "type": "Node" if isinstance(object, Node) else "Workflow",
                    "object": object.serialize()
                },
                headers = { "flowix_token": self.__token }
            ).json()["state"] == "success"
        except:
            return False
        
    def unshare(self, target:str | Node | Workflow) -> bool:
        try:
            return requests.post(
                self.__base_url + f"/delete/{self.id}/{target if isinstance(target, str) else target.id}",
                headers = { "flowix_token": self.__token }
            ).json()["state"] == "success"
        except:
            return False
        
    def unshare_all(self) -> bool:
        try:
            return requests.post(
                self.__base_url + f"/delete/{self.id}",
                headers = { "flowix_token": self.__token }
            ).json()["state"] == "success"
        except:
            return False
    
    def load(self, target:str) -> Node | Workflow:
        result = requests.get(
            self.__base_url + f"/share/{self.id}/{target}",
            headers = { "flowix_token": self.__token }
        ).json()

        if result["state"] == "fail":
            raise RuntimeError(result["message"])

        if result["object"]["type"] == "Node":
            return Node.deserialize(result["object"]["object"])
        else:
            return Workflow.deserialize(result["object"]["object"])
