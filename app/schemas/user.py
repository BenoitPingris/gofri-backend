from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.user import User
from pydantic import BaseModel, constr, validator

User_Pydantic = pydantic_model_creator(User, name='User')


class Login(BaseModel):
    username: constr(min_length=5, max_length=20)
    password: constr(min_length=6, max_length=50)


class Register(BaseModel):
    username: constr(min_length=5, max_length=20)
    password: constr(min_length=6, max_length=50)
    confirm: constr(min_length=6, max_length=50)

    @validator('confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v
