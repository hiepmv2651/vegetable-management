
from pydantic import BaseModel


class JSONResponseDefault(BaseModel):
    status: bool
    message: str
    data: dict | list | None = None

    class Config:
        from_attributes = True
