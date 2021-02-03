from app.models.base import Base
from tortoise import fields


class Fridge(Base):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(50, unique=True)
    user = fields.ForeignKeyField('models.User', related_name='fridge')

    class Meta:
        table = "fridges"


class FridgeFoods(Base):
    id = fields.UUIDField(pk=True)
    fridge = fields.ForeignKeyField('models.Fridge')
    food = fields.ForeignKeyField('models.Food')
    quantity = fields.IntField(default=1)

    class Meta:
        table = "fridge_foods"
