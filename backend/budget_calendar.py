import datetime
import utils


# A calendar which stores Day objects and maintains the relationship of
# balances between each day
class Calendar(object):

    def __init__(self, config):
        self.days = {}
        self.first_day = None
        self.last_day = None
        self.config = config

    def add_day(self, date):
        if type(date) is str:
            date_obj = utils.str_to_obj(date)
            date_str = date
        elif type(date) is datetime.date:
            date_obj = date
            date_str = str(date)
        else:
            raise TypeError('{} is not a valid date type'.format(date))

        if date_str not in self.days:
            self.days[date_str] = Day(self.config, date_obj)

        if not self.first_day or self.first_day > date_obj:
            self.first_day = date_obj
        else:
            pass

        if not self.last_day or self.last_day < date_obj:
            self.last_day = date_obj
        else:
            pass

    def add_transaction(self, account, transaction_obj):
        date_str = str(transaction_obj.date)
        if date_str not in self.days:
            self.add_day(date_str)
        else:
            pass

        self.days[date_str].add_transaction(account, transaction_obj)

    def update_running_balances(self, date=None):
        if type(date) is str:
            date_obj = utils.str_to_obj(date)
            first_day = date_obj
        elif type(date) is datetime.date:
            date_obj = date
            first_day = date_obj
        elif date is None:
            first_day = self.first_day
        else:
            raise TypeError('{} is not a valid date type'.format(date))

        last_day = self.last_day

        for cal_day in self.days_generator(first_day, last_day):
            if cal_day == self.first_day:
                for account in self.days[str(cal_day)].running_balance:
                    self.days[str(cal_day)].running_balance[account] += self.config.starting_bal[account]

                continue
            prev_day = self.get_prev_date(cal_day)

            for account in self.days[str(prev_day)].running_balance:
                prev_running_bal = self.days[str(prev_day)].running_balance[account]
                self.days[str(cal_day)].reset_running_bal(account, prev_running_bal)

    def days_generator(self, first_day, last_day):
        curr_day = first_day
        day_difference = last_day - first_day
        day_difference = day_difference.days + 1

        for index in range(day_difference):
            if str(curr_day) in self.days:
                yield curr_day
            elif curr_day > last_day:
                break

            curr_day += datetime.timedelta(1)

        return

    def get_prev_date(self, date):
        assert date != self.first_day, "No previous day exists for first day."

        prev_date = date - datetime.timedelta(1)

        while str(prev_date) not in self.days:
            prev_date = prev_date - datetime.timedelta(1)
            if prev_date < self.first_day:
                raise ValueError('Previous date exceeded lower bound of first day!')

        return prev_date


class Day(object):

    def __init__(self, config, date):

        self.date = date
        self.config = config
        self.running_balance = {}
        self.transactions = {}

    def add_transaction(self, account, transaction_obj):
        if account not in self.transactions:
            self.transactions[account] = list()
        else:
            pass

        if transaction_obj not in self.transactions[account]:
            self.transactions[account].append(transaction_obj)
        else:
            raise ValueError('Duplicate transactions!')

        self.update_running_balance(account, transaction_obj.amount)

    def update_running_balance(self, account, difference):

        assert account in self.config.accounts, "{} is not a valid account.".format(account)

        if account in self.running_balance:
            self.running_balance[account] += float(difference)
        elif account not in self.running_balance:
            self.running_balance[account] = 0.00 + float(difference)

    def reset_running_bal(self, account, prev_day_amount):
        self.running_balance[account] = prev_day_amount

        if account in self.transactions:
            for transaction in self.transactions[account]:
                self.running_balance[account] += transaction.amount

    def __str__(self):
        ret_str = '{}\n'.format(self.date)
        for account in self.running_balance:
            ret_str += '{}: {}\n'.format(account, self.running_balance[account])

        ret_str += '\n'

        return ret_str