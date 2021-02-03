from app.models.fridge import Fridge, FridgeFoods
import pydantic
from pydantic.types import constr

from tortoise.contrib.pydantic import pydantic_model_creator

Fridge_Pydantic = pydantic_model_creator(Fridge,
                                         name='Fridge',
                                         include=('id', 'name'))

FridgeFoods_Pydantic = pydantic_model_creator(FridgeFoods, name='FridgeFoods')


class CreateFridge(pydantic.BaseModel):
    name: constr(min_length=4, max_length=20, strip_whitespace=True)


class AddFood(pydantic.BaseModel):
    id: str
