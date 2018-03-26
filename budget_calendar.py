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

    # Retrieve all new transactions from files in the given directory. Return a
    # list of transaction objects
    # TODO: add open_transactions to parent class and make compatible with generic csvs
    def open_transactions(self):
        transactions = list()
        transaction_dir = self.config.app_directory + '/transactions'
        files_in_dir = os.listdir(transaction_dir)

        for transaction_file_name in files_in_dir:
            path_name = transaction_dir + '/' + transaction_file_name
            account = None
            begin_read = False

            for iden in self.config.app_dictionary['accounts']:

                if iden in path_name:
                    account = iden
                    break

            if not account:
                # TODO: Don't raise error. Add to logger instead.
                raise ValueError('Filename does not match a known account')

            with open(path_name) as transactions_file:

                for line in transactions_file:
                    line = line.rstrip('\r\n')
                    line = re.sub('(?<=[A-Z])(,)(?=[A-Z\s])', ' ', line)
                    line = line.split(',')

                    if 'Date' in line[0] and not begin_read:
                        line[0] = 'Date'
                        begin_read = True
                        self.config.app_dictionary['transaction_descriptors'][account] = line
                        continue

                    if begin_read:
                        tran = transaction.Transaction(account, line)
                        transactions.append(tran)

        self.update_cal(transactions)

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