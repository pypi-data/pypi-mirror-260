from pydantic import BaseModel, Extra


class Parameter(BaseModel):
    name: str
    value: float | int | str
    desc: str = ''

    class Config:
        extra = Extra.forbid
