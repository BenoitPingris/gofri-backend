from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.food import Food

Food_Pydantic = pydantic_model_creator(Food,
                                       name='Food',
                                       include=('id', 'name'))
