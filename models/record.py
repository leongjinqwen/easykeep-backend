import peewee as pw
from models.base_model import BaseModel
from models.assessment import Assessment
from models.account import Account


class Record(BaseModel):
    date = pw.DateField(null=False)
    account = pw.ForeignKeyField(Account, backref="records")
    assessment = pw.ForeignKeyField(Assessment, backref="records", on_delete="CASCADE")
    amount = pw.DecimalField(null=False, decimal_places=2)
    description = pw.TextField(null=True)
    reference = pw.TextField(null=True)