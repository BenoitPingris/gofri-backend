from fastapi import Request, Response, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth.auth_jwt import AuthJWT

from app.models.user import User


async def needs_jwt(req: Request = None, res: Response = None):
    jwt = AuthJWT(req, res)
    jwt.jwt_required()
    username = jwt.get_jwt_subject()
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await User.get(username=username)
    return user
