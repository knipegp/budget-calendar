# pylint: disable=missing-docstring
class Account:
    def __init__(self, name, starting_bal):
        self.name = name
        self.running_balance = starting_bal
        self._transactions = dict()
        self._sorted_keys = list()

    # Add a transaction to the current date
    def add_transaction(self, date, new_transaction):
        """

        :param date:
        :param new_transaction:
        :return:
        """

        if date not in self._transactions:
            self._transactions[new_transaction.date] = [new_transaction]
            self._sorted_keys.append(date)
            self._sorted_keys.sort()
        else:
            for tran in self._transactions[date]:
                if tran.csv == new_transaction.csv:
                    # log duplicate
                    return

            self._transactions[new_transaction.date].append(new_transaction)

    def update_running_bal(self, amount):
        self.running_balance += amount

    def get_transactions(self):
        ret = list()
        for date in self._sorted_keys:
            for transaction in self._transactions[date]:
                ret.append(transaction)

        return ret

    def get_sorted_keys(self):
        return self._sorted_keys
