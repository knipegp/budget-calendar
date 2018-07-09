import budget_calendar
import configuration
import os
import financial_transaction
import financial_account
import financial_statement


class Application(object):

    def __init__(self):
        self.config = configuration.AppConfiguration('budget-calendar')
        self.calendar = budget_calendar.Calendar(self.config)
        self.accounts = dict()

        for account in self.config.accounts:
            self.accounts.update({account: financial_account.Account(account, self.config.starting_bal[account])})

    def run(self):
        self.add_transactions_from_statements()

    def add_transactions_from_statements(self):
        statements = list()
        statement_files = os.listdir(self.config.transaction_directory)

        for new_file in statement_files:
            statements.append(financial_statement.Statement(new_file, self.config))

        for statement in statements:
            account = statement.account
            for transaction in statement.rows:
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
                self.accounts[account].add_transaction(new_transaction)
                self.accounts[account].update_running_bal(new_transaction.amount)


if __name__ == '__main__':
    app = Application()
    app.run()
