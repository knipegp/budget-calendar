import datetime
import configuration


# Class for transactions read from bank statements
class Transaction:

    def __init__(self, account, data_dict=None):
        self.data = dict()

        # TODO: Get rid of multiple instances of the same config
        self.config = configuration.AppConfiguration('budget_calendar')

        # Add the transaction descriptors to the transaction if the account already exists
        try:
            for descriptor in self.config.app_dictionary['transaction_descriptors'][account]:
                self.data.update({descriptor: None})
        except KeyError:
            # Add the account to the configuration if it doesn't exist yet
            print 'Account {} has not been instantiated.'.format(account)
            self.config.add_account(account)

        if data_dict:
            self.data = data_dict

        else:
            self.create_transaction()

        self.date = configuration.str_to_obj(self.data['Date'])

    def __str__(self):
        save_text = ''

        for key in sorted(self.data):
            save_text += str(self.data[key]) + ','

        save_text = save_text[:-1]

        return save_text

    # TODO: Change to load data dictionary from csv
    def get_from_line(self, line):

        if not self.data['Amount'] and self.data['Running Bal.']:
            self.data['Amount'] = self.data['Running Bal.']

        elif not self.data['Amount']:
            self.data['Amount'] = '0'

    def create_transaction(self):

        for key in self.data:

            self.data[key] = configuration.get_free_answer('Enter information to fill transaction field "{}": '.format(key))

    # def update_descriptor(self):
