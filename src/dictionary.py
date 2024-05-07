from enum import Enum

class Languages(Enum):
    FA:0
    ENG:1
class MultiLangMessage():
    messages:dict
    def __init__(self,messages:dict) -> None:
        for key in messages:
            if key not in Languages:
                Exception(f"{key} not found languages config")
        self.messages = messages
dictionary={
    "user":MultiLangMessage({Languages.FA:"کاربران",Languages.ENG:"Users"})
}