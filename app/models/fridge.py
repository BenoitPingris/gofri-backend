from tortoise import fields
from tortoise.models import Model


class Fridge(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='fridge')
    name = fields.CharField(50, unique=True)

    class Meta:
        table = "fridges"


class FridgeFoods(Model):
    id = fields.UUIDField(pk=True)
    fridge = fields.ForeignKeyField('models.Fridge')
    foods = fields.ForeignKeyField('models.Food')
    quantity = fields.IntField()

    class Meta:
        table = "fridge_foods"
