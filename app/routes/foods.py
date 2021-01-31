from fastapi import APIRouter, UploadFile, File, Depends, status, Form
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from tortoise.exceptions import DoesNotExist
from app.models.food import Food
from app.schemas.foods import Food_Pydantic
import time
from app.config import get_settings

router = APIRouter(prefix='/foods', tags=['foods'])


@router.get('')
async def fetch_images():
    return await Food_Pydantic.from_queryset(Food.all())


@router.get('/{id}/image')
async def get_image(id: str):
    try:
        food = await Food.get(id=id)
        return FileResponse(food.photo_path)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post('')
async def create_food(name: str = Form(...),
                      photo: UploadFile = File(...),
                      Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    admin = Authorize.get_raw_jwt()['admin']
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    media = get_settings().media_url
    file_location = f'{media}/{round(time.time() * 10000)}'

    with open(file_location, 'wb+') as f:
        f.write(photo.file.read())
    food_created = await Food.create(name=name, photo_path=file_location)
    return food_created
