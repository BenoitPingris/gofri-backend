from typing import Any, Type, Union
from fastapi import status
from fastapi.exceptions import HTTPException
from tortoise.models import Model
from tortoise.query_utils import Q


class Base(Model):
    @classmethod
    async def get_or_404(cls: Type[Model], *args: Q,
                         **kwargs: Any) -> Union[Model, None]:
        data = await cls.get_or_none(*args, **kwargs)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return data
