# TODO: write docstrings
# pylint: disable=missing-docstring
import datetime
from . import utils


# Class for _transactions read from bank statements
class Transaction:
    def __init__(self, date=None, amount=None, description=None, account=None):
        self.amount = amount
        self.description = description
        self.account = account

        # TODO: isinstance code smell
        if isinstance(date, str):
            self.date = utils.correct_date(date)
        # TODO: isinstance code smell
        elif isinstance(date, datetime.date) or date is None:
            self.date = date
        else:
            raise TypeError("date is of incorrect type {}".format(type(date)))

    @property
    def csv(self):
        return ",".join([str(self.date), self.description, str(self.amount)])

    @property
    def data_dict(self):
        return {
            "date": str(self.date),
            "description": self.description,
            "amount": str(self.amount),
        }
