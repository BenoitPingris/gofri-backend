from app.schemas.fridge import CreateFridge
from fastapi.exceptions import HTTPException
from app.deps.jwt import needs_jwt
from app.models.user import User
from fastapi import APIRouter, status
from fastapi.param_functions import Depends
from typing import cast

from tortoise.exceptions import IntegrityError
from app.models.fridge import Fridge, FridgeFoods
from app.models.food import Food

router = APIRouter(prefix='/fridges', tags=['fridges'])


@router.get('')
async def fetch_fridges(user: User = Depends(needs_jwt)):
    return await Fridge.filter(user=user)


@router.get('/{fridge_id}')
async def get_fridge(fridge_id: str, user: User = Depends(needs_jwt)):
    fridge = cast(Fridge, await Fridge.get_or_404(id=fridge_id))
    fridge_foods = FridgeFoods.filter(fridge_id=fridge.id)
    return await fridge_foods.prefetch_related('food')


@router.post('')
async def create_fridge(name: CreateFridge, user: User = Depends(needs_jwt)):
    try:
        created_fridge = await Fridge.create(name=name.name, user=user)
        return created_fridge
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.delete('/{id}')
async def delete_fridge(id: str, user: User = Depends(needs_jwt)):
    fridge = await Fridge.get_or_404(id=id)
    return await fridge.delete()


@router.post('/{fridge_id}/food/{food_id}')
async def add_food(fridge_id: str,
                   food_id: str,
                   user: User = Depends(needs_jwt)):
    fridge = await Fridge.get_or_404(id=fridge_id)
    if fridge.user_id != user.id:  # type:ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    food = await Food.get_or_404(id=food_id)
    return await FridgeFoods.create(fridge=fridge, food=food, quantity=1)
