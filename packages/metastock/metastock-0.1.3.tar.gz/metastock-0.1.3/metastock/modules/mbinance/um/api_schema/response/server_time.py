from pydantic import BaseModel


class ServerTime(BaseModel):
    serverTime: int
