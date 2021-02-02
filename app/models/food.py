from app.models.base import Base
from tortoise import fields


class Food(Base):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(25, unique=True)
    photo_path = fields.CharField(255)
    created_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "foods"
