import bcrypt
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException


def hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt())


class Settings(BaseModel):
    authjwt_secret_key: str = "ptdrbruh"


def setup_jwt(app: FastAPI):
    @AuthJWT.load_config
    def get_config():
        return Settings()

    @app.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, ex: AuthJWTException):
        return JSONResponse(status_code=ex.status_code,
                            content={'detail': ex.message})
