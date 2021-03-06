from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.routes import auth, foods, fridge, ping
from app.services.auth import setup_jwt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(ping.router)
app.include_router(foods.router)
app.include_router(auth.router)
app.include_router(fridge.router)

setup_jwt(app)

register_tortoise(app,
                  db_url='sqlite://gofri.sqlite3',
                  modules={
                      'models': [
                          'app.models.user',
                          'app.models.food',
                          'app.models.fridge',
                      ]
                  },
                  generate_schemas=True)
