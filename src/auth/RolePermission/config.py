from pydantic_settings import BaseSettings
from enum import Enum,Flag,auto
from dataclasses import dataclass
class CRUD(Enum):
    CREATE="CREATE"
    READ="READ"
    UPDATE="UPDATE"
    DELETE="DELETE"
class Languages(Flag):
    FA="fa"
    ENG="eng"
class MultiLangMessage():
    messages:dict

    def __init__(self,messages:dict) -> None:
        
        self.messages = self.validate_messages(messages)

    def validate_messages(self,messages:dict):
        for key in messages:
            if key not in Languages:
                Exception(f"{key} not found languages config")
        return messages


@dataclass
class permission:
    id:int
    name:MultiLangMessage
    actions:list[str] = None

permission_conf: {permission} = {
    "user":permission(
        id=1,
        name=MultiLangMessage({Languages.FA:"کاربران",Languages.ENG:"Users"}),
        actions = [action.value for action in CRUD]
    ),
    "roles":permission(
        id=2,
        name=MultiLangMessage({Languages.FA:"نقش ها و دسترسی ها",Languages.ENG:"Roles and permissions"}),
        actions = [action.value for action in CRUD]
    ),
    "users-roles":permission(
        id=3,
        name=MultiLangMessage({Languages.FA:"نقش ادمین ها",Languages.ENG:"Users Roles"}),
        actions = [action.value for action in CRUD]
    )

}


