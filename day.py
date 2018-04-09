

# An object that stores a list of transaction objects
class Day(object):

    def __init__(self, date):
        self.date = date
        self.data = dict()
        self.data['transactions_per_account'] = {}
        self.data['running_balance_per_account'] = {}

    def __str__(self):
        print_str = ''
        print_str += '\nDate,' + str(self.date) + '\n'

        for key in self.data:

            if key == 'transactions_per_account':

                for account in self.data[key]:

                    for transaction in self.data[key][account]:
                        print_str += transaction.__str__()
                        print_str += '\n'

            else:
                print_str += '{}: {}\n'.format(key, self.data[key])

        print_str = print_str[:-2]

        return print_str

    def update_running_bal(self, previous_day_obj):
        ''' Update the running balances in a Day.

        :param previous_day_obj: A Day object for the previous day.
        :return: 0 if the function executes without errors.
                 1 if the function executes with an error.

        '''

        current_transactions = self.data['transactions_per_account']
        current_running_balances = self.data['running_balance_per_account']

        if previous_day_obj:
            previous_running_balance = previous_day_obj.data['running_balance_per_account']

            # Add accounts to running balance if they exist in the previous
            # day or are included in the Current Day's transactions
            for account in previous_running_balance:

                if account not in current_running_balances:
                    current_running_balances[account] = previous_running_balance[account]

        # TODO: This is hacky. Needs to get fixed or moved
        for account in current_transactions:

                for transaction in current_transactions[account]:
                    if account not in current_running_balances and 'Description' in transaction.data and 'Beginning' in transaction.data['Description']:
                        new_running_balance = transaction.data['Running Bal.']
                        current_running_balances[account] = new_running_balance
                        continue
                    elif account not in current_running_balances:
                        current_running_balances[account] = '0.00'

                    new_running_balance = str(round(float(transaction.data['Amount'])\
                                                    + float(current_running_balances[account]), 2))
                    current_running_balances[account] = new_running_balance

        return 0

    # Add a transaction to the current date
    def add_transaction(self, tran):

        # Check that transaction is being added to the correct date object
        if tran.data['Date'] != self.date:
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
