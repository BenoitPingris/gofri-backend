from tortoise import fields
from tortoise.models import Model
import bcrypt


class User(Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(25, unique=True)
    password = fields.BinaryField()
    admin = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password)
