import peewee as pw
from models.base_model import BaseModel
from models.user import User


class Business(BaseModel):
    name = pw.CharField(null=False)
    user = pw.ForeignKeyField(User, backref="businesses", on_delete="CASCADE")