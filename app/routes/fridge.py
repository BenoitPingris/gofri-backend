from app.schemas.fridge import CreateFridge
from fastapi.exceptions import HTTPException
from starlette import status
from app.deps.jwt import needs_jwt
from app.models.user import User
from fastapi import APIRouter
from fastapi.param_functions import Depends

from tortoise.exceptions import IntegrityError
from app.models.fridge import Fridge

router = APIRouter(prefix='/fridges', tags=['fridges'])


@router.get('')
async def get_fridge(user: User = Depends(needs_jwt)):
    return await Fridge.filter(user=user)


@router.post('')
async def create_fridge(name: CreateFridge, user: User = Depends(needs_jwt)):
    try:
        created_fridge = await Fridge.create(name=name, user=user)
        return created_fridge
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.delete('/{id}')
async def delete_fridge(id: str, user: User = Depends(needs_jwt)):
    fridge = await Fridge.get_or_none(id=id)
    if not fridge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await fridge.delete()


@router.post('/{id}/food')
async def add_food(user: User = Depends(needs_jwt)):
    pass
