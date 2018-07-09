import logging


class Account(object):

    def __init__(self, name, starting_bal=0.0):
        self.name = name
        self.running_balance = starting_bal
        self.transactions = dict()

    # Add a transaction to the current date
    def add_transaction(self, transaction):
        """

        :param transaction:
        :return:
        """
        assert transaction.account == self.name, 'Transaction {} account {}'\
                                                 'is not in account {}'.format(transaction.csv,
                                                                               transaction.account,
                                                                               self.name)
        if transaction.date not in self.transactions:
            self.transactions[transaction.date] = [transaction]
        else:
            for tran in self.transactions[transaction.date]:
                if tran.csv == transaction.csv:
                    # log duplicate
                    return

            self.transactions[transaction.date].append(transaction)

    def update_running_bal(self, amount):
        self.running_balance += amount
