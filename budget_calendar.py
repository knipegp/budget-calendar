import configuration
import calendar
import datetime
import day
import transaction
import os
import logging
import re


class BudgetCalendar(calendar.Calendar):

    def __init__(self):
        super(BudgetCalendar, self).__init__('budget_calendar')

    def add_new_transaction(self):
        new_transactions = list()
        # Ask to pick which account
        print 'Possible accounts: {}'.format(self.config.app_dictionary['accounts'])
        possible_answers = self.config.app_dictionary['accounts'] + 'new'
        account = configuration.get_free_answer('Choose an account to add the transaction or enter new? [account/new]: ', 0, possible_answers)

        if account == 'new':
            account = configuration.get_free_answer('Enter new account name: ', 1)

        tran = transaction.Transaction(account)
        new_transactions.append(tran)

        # Create repeated transactions
        ans = configuration.get_binary_answer('Does this transaction repeat?')

        # Need to make the date repeating more intelligent
        if ans:
            dates = configuration.get_free_answer('Enter repeat date: [yyyy/mm/dd]', 0)

            for date in dates:
                new_date = date.split('/')

        self.update_cal(new_transactions)

    # Add transactions to the calendar and update the necessary values
    def update_cal(self, transactions):
        # Need to account for when only 1 transaction is passed
        trans = list()
        trans = trans + transactions

        for tran in trans:

            if str(tran.date) not in self.days:
                self.days[str(tran.date)] = day.Day(tran.date)

            self.days[str(tran.date)].add_transaction(tran)

        self.update_running_bal()
        self.config.write_config()


def main():
    cal = calendar.Calendar()
    cal.open_transactions()
    cal.print_calendar()
    # cal.save_calendar()
    # cal.days['2018-02-08'].print_date()


if __name__ == "__main__":
    main()