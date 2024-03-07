from pydantic import BaseModel


class Config(BaseModel):
    lolmatch_command_priority: int = 10
