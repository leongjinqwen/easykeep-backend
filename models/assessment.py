import peewee as pw
from models.base_model import BaseModel
from models.business import Business


class Assessment(BaseModel):
    business = pw.ForeignKeyField(Business, backref="assessments", on_delete="CASCADE")
    year_assessment = pw.CharField(null=False)
    year_ended = pw.DateField(null=False)