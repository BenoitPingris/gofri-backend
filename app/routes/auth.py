from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from app.models.user import User
from app.schemas.user import User_Pydantic, Register, Login
from app.services.auth import hash
from tortoise.exceptions import DoesNotExist

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register')
async def register(user: Register):
    if await User.exists(username=user.username):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_created = await User.create(username=user.username,
                                     password=hash(user.password))
    return await User_Pydantic.from_tortoise_orm(user_created)


@router.post('/token')
async def login(data: Login, Authorize: AuthJWT = Depends()):
    try:
        user = await User.get(username=data.username)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if user.verify_password(data.password):
        access_token = Authorize.create_access_token(
            subject=user.username, user_claims={'admin': user.admin})
        refresh_token = Authorize.create_refresh_token(subject=user.username)

        return {'access_token': access_token, 'refresh_token': refresh_token}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    admin = Authorize.get_raw_jwt()['admin']
    new_access_token = Authorize.create_access_token(
        subject=current_user, user_claims={'admin': admin})
    return {"access_token": new_access_token}


@router.get('/me')
async def me(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    me = Authorize.get_jwt_subject()
    return me
