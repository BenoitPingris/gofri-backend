from fastapi import FastAPI
from .routes import ping, foods, auth, fridge
from tortoise.contrib.fastapi import register_tortoise
from .services.auth import setup_jwt

app = FastAPI()

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
