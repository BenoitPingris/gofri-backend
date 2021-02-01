import pydantic
from pydantic.types import constr


class CreateFridge(pydantic.BaseModel):
    name: constr(min_length=4, max_length=20, strip_whitespace=True)


class AddFood(pydantic.BaseModel):
    id: str
