

# An object that stores a list of transaction objects
class Day(object):

    def __init__(self, date):
        self.date = date
        self.data = dict()
        self.data['transactions_per_account'] = {}
        self.data['running_balance_per_account'] = {}

    def print_day(self):
        print_str = ''
        print_str += '\nDate,' + str(self.date)

        for key in self.data:
            print_str += '\n   {}: {}'.format(key, self.data[key])

        print print_str
        return print_str

    def update_running_bal(self, previous_day_obj):
        ''' Update the running balances in a Day.

        :param previous_day_obj: A Day object for the previous day.
        :return: 0 if the function executes without errors.
                 1 if the function executes with an error.

        '''

        current_transactions = self.data['transactions_per_account']
        current_running_balances = self.data['running_balance_per_account']

        if not previous_day_obj:

            for account in current_transactions:

                for transaction in current_transactions[account]:

                    # TODO: This is bad. Find new way to initialize running Bal
                    if 'Running Bal.' in transaction.data:
                        current_running_balances[account] = transaction.data['Running Bal.']
                        break
                    else:
                        current_running_balances[account] = '0.00'

        else:
            previous_running_balance = previous_day_obj.data['running_balance_per_account']

            # Add accounts to running balance if they exist in the previous
            # day or are included in the Current Day's transactions
            for account in previous_running_balance:

                if account not in current_running_balances:
                    current_running_balances[account] = previous_running_balance[account]

        for account in current_transactions:

            for transaction in current_transactions[account]:
                account = transaction.data['Account']

                if account not in current_running_balances:
                    current_running_balances[account] = '0.00'

                new_running_balance = str(round(float(transaction.data['Amount'])\
                                                + float(current_running_balances[account]), 2))
                current_running_balances[account] = new_running_balance

        return 0

    # Add a transaction to the current date
    def add_transaction(self, tran):

        # Check that transaction is being added to the correct date object
        if tran.date != self.date:
            return 1

        # Add the account to that date if it does not exist
        if tran.data['Account'] not in self.data['transactions_per_account']:
            self.data['transactions_per_account'][tran.data['Account']] = list()

        # Skip transactions that have already been added
        else:
            for existing_transaction in self.data['transactions_per_account'][tran.data['Account']]:

                if tran.data == existing_transaction.data:

                    return False

        self.data['transactions_per_account'][tran.data['Account']].append(tran)

        return True
