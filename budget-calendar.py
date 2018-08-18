import os
from backend import financial_statement, financial_transaction, budget_calendar, configuration, financial_account


DIR = os.path.dirname(os.path.realpath(__file__))


class Application(object):

    def __init__(self):
        self.config = configuration.AppConfiguration('budget-calendar', DIR)
        self.calendar = budget_calendar.Calendar(self.config)
        self.accounts = dict()

        for account in self.config.accounts:
            self.accounts.update({account: financial_account.Account(account, self.config.starting_bal[account])})

    def run(self):
        self.add_transactions_from_statements()
        self.save()

    def add_transactions_from_statements(self):
        statements = list()
        statement_files = os.listdir(self.config.transaction_directory)

        for new_file in statement_files:
            file_path = os.path.join(self.config.transaction_directory, new_file)
            account = self.get_statement_account(file_path)
            new_statement = financial_statement.ReadStatement(file_path, account)
            statements.append(new_statement)

        for statement in statements:
            account = statement.account
            for transaction in statement.get_rows():
                date = None
                description = None
                amount = None
                for key in transaction:
                    if 'date' in key.lower():
                        date = transaction[key]
                    elif 'payee' in key.lower() or 'description' in key.lower():
                        description = transaction[key]
                    elif 'amount' in key.lower():
                        if not transaction[key]:
                            amount = 0.0
                        else:
                            amount = float(transaction[key])

                assert None not in [date, description, amount],\
                    "Transaction {} was not read correctly.".format(str(transaction))
                new_transaction = financial_transaction.Transaction(date, amount, description, account)
                self.accounts[account].add_transaction(new_transaction.date, new_transaction)
                self.accounts[account].update_running_bal(new_transaction.amount)

    def get_statement_account(self, filename):
        ret = None
        for account in self.config.accounts:
            if account in filename:
                ret = account

        assert ret, '{} does not belong to an account'.format(filename)

        return ret

    def save(self):
        for account in self.accounts:
            file_path = os.path.join(self.config.saved_transaction_directory, 'account_{}.csv'.format(account))
            new_statement = financial_statement.WriteStatement(file_path, account)
            rows = list()
            for transaction in self.accounts[account].get_transactions():
                rows.append(transaction.data_dict)

            new_statement.write(rows)


def main():
    app = Application()
    app.run()


if __name__ == '__main__':
    main()
