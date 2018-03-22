import configuration
import calendar
import datetime
import transaction
import os
import logging
import re


class BudgetCalendar(calendar.Calendar):

    def __init__(self):
        super(BudgetCalendar, self).__init__('budget_calendar')

    # Update the running balance of each account of each day based on the
    # transactions added to each day of the calendar
    def update_running_bal(self, use_first=False, start_day=None):

        # The calendar could use the first day of the first month but that day
        # may not actually have any transactions
        if use_first:
            start_day = self.first_day

        assert start_day is not None, 'Specify start day or use self.first_day'

        # Need a timedelta object to iterate days
        date_diff = datetime.timedelta(days=1)
        curr_day = start_day

        # Iterate over all days in the calendar
        while curr_day <= self.last_day:

            # Get the string of the previous day
            curr_day_obj = self.str_to_obj(curr_day)
            prev_day = str(curr_day_obj - date_diff)

            for acc in self.days[curr_day].account_totals:

                # If starting from the first day
                # or the account exists in current_day and not in prev_day
                if curr_day == self.first_day\
                        or acc not in self.days[prev_day].account_running_bal\
                        and acc in self.days[curr_day].account_totals:
                    # if acc == 'checkings':

                    for transaction in self.days[curr_day].account_trans[acc]:
                        try:
                            if 'Beginning balance' in transaction.data['Description']:

                                self.days[curr_day].account_running_bal[acc] = round(float(transaction.data['Running Bal.']), 2)\
                                                                               + self.days[curr_day].account_totals[acc]
                                break
                        except:
                            self.days[curr_day].account_running_bal[acc] = self.days[curr_day].account_totals[acc]
                            break
                # If acc in curr and in prev
                else:
                    self.days[curr_day].account_running_bal[acc] = self.days[curr_day].account_totals[acc]\
                                                                   + self.days[prev_day].account_running_bal[acc]

            # Can only update balances if yesterday exists
            if curr_day != self.first_day:

                for acc in self.days[prev_day].account_totals:

                    # If acc in prev but not in curr
                    if acc in self.days[prev_day].account_running_bal\
                            and acc not in self.days[curr_day].account_totals:

                        self.days[curr_day].account_running_bal[acc] = self.days[prev_day].account_running_bal[acc]
                        self.days[curr_day].account_totals[acc] = 0.00

            curr_day = str(curr_day_obj + date_diff)

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
                self.days[str(tran.date)] = BudgetDay(tran.date)

            self.days[str(tran.date)].add_transaction(tran)

        self.complete_calendar()
        self.update_running_bal(True)
        self.config.write_config()


class BudgetDay(calendar.Day):

    ''' TODO: All of day data should be in a single dictionary to make it easier for the super to handle
    different types of applications without much overhead
    '''
    def __init__(self, date):
        self.account_trans = {}
        self.account_totals = {}
        self.account_running_bal = {}
        super(BudgetDay, self).__init__(date)

    # Add a transaction to the current date
    def add_transaction(self, tran):

        # Check that transaction is being added to the correct date object
        if tran.date != self.date:
            logging.debug("Transaction date {} does not match Day date {}.".format(tran.date, self.date))
            return False

        # Add the account to that date if it does not exist
        if tran.data['Account'] not in self.account_trans:
            self.account_trans[tran.data['Account']] = list()
            self.account_totals[tran.data['Account']] = 0.00

            #TODO: update the running balance here? Not set on this
            self.account_running_bal[tran.data['Account']] = 0.00

        # Skip transactions that have already been added
        else:
            for existing_transaction in self.account_trans[tran.data['Account']]:

                if tran.data == existing_transaction.data:

                    return False

        self.account_trans[tran.data['Account']].append(tran)
        self.account_totals[tran.data['Account']] += round(float(tran.data['Amount']), 2)

        return True


def main():
    cal = calendar.Calendar()
    cal.open_transactions()
    cal.print_calendar()
    # cal.save_calendar()
    # cal.days['2018-02-08'].print_date()


if __name__ == "__main__":
    main()