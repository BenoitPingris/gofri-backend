from app.schemas.fridge import (CreateFridge, FridgeFoods_Pydantic,
                                Fridge_Pydantic)
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
    return await Fridge_Pydantic.from_queryset(Fridge.filter(user=user))


@router.get('/{fridge_id}')
async def get_fridge(fridge_id: str, user: User = Depends(needs_jwt)):
    fridge = cast(Fridge, await Fridge.get_or_404(id=fridge_id))
    fridge_foods = FridgeFoods.filter(fridge_id=fridge.id)
    return await fridge_foods.values('quantity', 'food__id', 'food__name')


@router.post('')
async def create_fridge(name: CreateFridge, user: User = Depends(needs_jwt)):
    try:
        created_fridge = await Fridge.create(name=name.name, user=user)
        return await Fridge_Pydantic.from_tortoise_orm(created_fridge)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.delete('/{id}')
async def delete_fridge(id: str, user: User = Depends(needs_jwt)):
    fridge = await Fridge.get_or_404(id=id)
    await fridge.delete()
    return 'ok'


@router.post('/{fridge_id}/food/{food_id}')
async def add_food(fridge_id: str,
                   food_id: str,
                   user: User = Depends(needs_jwt)):
    fridge = await Fridge.get_or_404(id=fridge_id)
    if fridge.user_id != user.id:  # type:ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    food = await Food.get_or_404(id=food_id)
    fridge_food, created = await FridgeFoods.get_or_create(fridge=fridge,
                                                           food=food)
    if not created:
        fridge_food.quantity
        fridge_food.update_from_dict({'quantity': fridge_food.quantity + 1})
        await fridge_food.save()
    return await FridgeFoods_Pydantic.from_tortoise_orm(fridge_food)


@router.delete('/{fridge_id}/food/{food_id}')
async def remove_food(fridge_id: str,
                      food_id: str,
                      user: User = Depends(needs_jwt)):
    fridge = await Fridge.get_or_404(id=fridge_id)
    if fridge.user_id != user.id:  # type:ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    food = await Food.get_or_404(id=food_id)
    fridge_food = cast(FridgeFoods, await FridgeFoods.get_or_404(fridge=fridge,
                                                                 food=food))
    if fridge_food.quantity == 1:
        return await fridge_food.delete()
    fridge_food.update_from_dict({'quantity': fridge_food.quantity - 1})
    return await fridge_food.save()
