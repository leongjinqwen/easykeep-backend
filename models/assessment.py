import peewee as pw
from models.base_model import BaseModel
from models.business import Business


class Assessment(BaseModel):
  business = pw.ForeignKeyField(Business, backref="assessments", on_delete="CASCADE")
  year_assessment = pw.CharField(null=False)
  year_ended = pw.DateField(null=False)

  def total(self):
    from models.record import Record
    from models.account import Account
    '''
    sample result = { 
      1: {'total': 2000.0, 
        'list': [
          {'account_id': 15, 'account_name': 'Equipment', 'account_type': 1, 'account_number': '2000-100', 'amount': 2000.0}
        ]}, 
      2: {'total': 1600.0, 
        'list': [
          {'account_id': 8, 'account_name': 'Cash in Hand', 'account_type': 2, 'account_number': '3200-000', 'amount': -1400.0}, 
          {'account_id': 14, 'account_name': 'Cash At Bank', 'account_type': 2, 'account_number': '3100-000', 'amount': -1950.0}
        ]}, 
      ...
    }
    '''
    result = {} 
    for i in range(9):
      records = Record.select().join(Account).where(Account.acc_type == i, Record.assessment == self.id)
      check_list = []
      for r in records:
        if not result.get(r.account.acc_type):
          result[r.account.acc_type] = {}
          result[r.account.acc_type]['total'] = 0
          result[r.account.acc_type]['list'] = []
        result[r.account.acc_type]['total'] += (r.amount / 100)
        if not r.account.id in check_list:
          check_list.append(r.account.id)
          result[r.account.acc_type]['list'].append({
            'account_id' : r.account.id,
            'account_name' : r.account.name,
            'account_type' : r.account.acc_type,
            'account_number' : r.account.account_number,
            'amount' : (r.amount / 100)
          })
        else:
          for acc in result[r.account.acc_type]['list']:
            if r.account.id == acc['account_id'] :
              acc['amount'] = ((acc['amount'])+ (r.amount / 100))
    return result

