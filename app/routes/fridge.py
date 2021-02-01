from fastapi.exceptions import HTTPException
from starlette import status
from app.deps.jwt import needs_jwt
from app.models.user import User
from fastapi import APIRouter
from fastapi.param_functions import Depends

from app.models.fridge import Fridge

router = APIRouter(prefix='/fridge')


@router.get('')
async def get_fridge(user: User = Depends(needs_jwt)):
    return await Fridge.filter(user=user)


@router.post('')
async def create_fridge(user: User = Depends(needs_jwt)):
    created_fridge = await Fridge.create(user=user)
    return created_fridge


@router.delete('/{id}')
async def delete_fridge(id: str, user: User = Depends(needs_jwt)):
    fridge = await Fridge.get_or_none(id=id)
    if not fridge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await fridge.delete()
