import datetime
import utils


# Class for transactions read from bank statements
class Transaction:

    def __init__(self, date=None, amount=None, description=None, account=None):
        self.amount = amount
        self.description = description
        self.account = account

        if type(date) is str:
            self.date = utils.correct_date(date)
        elif type(date) is datetime.date or date is None:
            self.date = date
        else:
            raise TypeError('date is of incorrect type {}'.format(type(date)))

    @property
    def csv(self):
        return ','.join([str(self.date), self.description, str(self.amount)])
