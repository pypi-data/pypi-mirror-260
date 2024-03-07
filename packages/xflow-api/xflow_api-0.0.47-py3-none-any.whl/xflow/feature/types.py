import numpy
from pydantic import BaseModel


class DatasetElementInfo(BaseModel):
    NAME: str
    DIMS: list
    TYPE: str
    DESC: str
    FEATURE_NAMES: list = []


class DatasetComposition(BaseModel):
    DATA: list[DatasetElementInfo]
    LABEL: list = []


class DatasetElement(BaseModel):
    name: str
    data: numpy.ndarray
    desc: str = ''
    feature_names: list = []

    class Config:
        arbitrary_types_allowed = True


