from _typeshed import Incomplete
from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    class Config:
        allow_population_by_field_name: bool
        extra: Incomplete
        use_enum_values: bool
