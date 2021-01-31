from fastapi import FastAPI
from .routes import ping, foods, auth
from tortoise.contrib.fastapi import register_tortoise
from .services.auth import setup_jwt

app = FastAPI()

app.include_router(ping.router)
app.include_router(foods.router)
app.include_router(auth.router)

setup_jwt(app)


register_tortoise(
    app,
    db_url='sqlite://gofri.sqlite3',
    modules={
        'models': ['app.models.user']
    },
    generate_schemas=True
)
