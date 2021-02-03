from typing import cast
from app.deps.jwt import needs_jwt
from app.models.user import User
from fastapi import APIRouter, UploadFile, File, Depends, status, Form
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from tortoise.exceptions import IntegrityError
from app.models.food import Food
from app.schemas.foods import Food_Pydantic
import time
from app.config import get_settings

router = APIRouter(prefix='/foods', tags=['foods'])


@router.get('')
async def fetch_foods():
    return await Food_Pydantic.from_queryset(Food.all())


@router.delete('/{id}')
async def delete_food(id: str, user: User = Depends(needs_jwt)):
    food = await Food.get_or_404(id=id)
    await food.delete()
    return 'ok'


@router.get('/{id}/image')
async def get_image(id: str):
    food = cast(Food, await Food.get_or_404(id=id))
    return FileResponse(food.photo_path)


@router.post('')
async def create_food(name: str = Form(...),
                      photo: UploadFile = File(...),
                      user: User = Depends(needs_jwt)):
    # if not user.admin:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    media = get_settings().media_url
    file_location = f'{media}/{round(time.time() * 10000)}'

    try:
        with open(file_location, 'wb+') as f:
            f.write(photo.file.read())
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:
        food_created = await Food.create(name=name, photo_path=file_location)
        return await Food_Pydantic.from_tortoise_orm(food_created)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
