import peewee as pw
from models.base_model import BaseModel
from models.business import Business
from enum import Enum


class Account(BaseModel):
    class AccType(Enum):
        EQUITY = 0
        FIXED_ASSETS = 1
        CURRENT_ASSETS = 2
        LONG_TERM_LIABILITIES = 3
        CURRENT_LIABILITIES = 4
        SALES = 5
        OTHER_INCOMES = 6
        PURCHASES = 7
        EXPENSES = 8

    business = pw.ForeignKeyField(Business, backref="accounts", on_delete="CASCADE")
    name = pw.CharField(null=False)
    account_number = pw.CharField(null=False)
    acc_type = pw.IntegerField(null=False)