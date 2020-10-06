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

  def monthly_pnl(self):
    from models.record import Record
    from models.account import Account

    '''sample output : a list of object
    [
      { month: 'Jan', np: 200, gp: 300, exp:100 , revenue: 500, cos: 200 },
      { month: 'Feb', np: 133, gp: 233, exp:100 , revenue: 333, cos: 100 },
    ]
    '''
    # only profit/loss accounts ((5+6)-(7+8))
    # get all records according to months
    month_list = []
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for m in range(1,13):
      result = {}
      result['month'] = months[m-1]
      result['np'] = 0
      result['revenue'] = 0
      result['exp'] = 0
      for i in range(5,9):
        records = Record.select().join(Account).where(Account.acc_type == i, Record.date.month == m, Record.assessment == self.id)
        for r in records:
          result['np'] -= r.amount/100
          if r.account.acc_type in [5,6]: result['revenue'] -= r.amount/100
          if r.account.acc_type in [7,8]: result['exp'] += r.amount/100
      month_list.append(result)
    return month_list


