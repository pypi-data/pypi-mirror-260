from pydantic import BaseModel


class TagRead(BaseModel):
    id: str
    org_id: str
    name: str
    description: str


class TagCreate(BaseModel):
    name: str
    description: str = ""


class TagUpdate(BaseModel):
    description: str | None = None
