import datetime
import configuration


# Class for transactions read from bank statements
class Transaction:

    def __init__(self, account, line=None):
        self.data = dict()

        self.data['Account'] = account
        self.config = configuration.AppConfiguration('budget_calendar')

        # Add the transaction descriptors to the transaction if the account already exists
        try:
            for descriptor in self.config.app_dictionary['transaction_descriptors'][account]:
                self.data.update({descriptor: None})
        except:
            # Add the account to the configuration if it doesn't exist yet
            print 'Account {} has not been instantiated.'
            self.config.add_account(account)

        if line:
            self.data['Actual'] = True
            self.get_from_line(line, account)

        elif not line:
            self.create_transaction()

        else:
            print 'Transaction passed:'
            print 'Line: ' + str(line)
            print 'Account: ' + str(self.config['Account'])
            raise StandardError('Transaction not instantiated with valid information')

        date = self.data['Date']
        month, day, year = date.split('/')
        self.date = datetime.date(int(year), int(month), int(day))

    def print_transaction(self):
        save_text = '\n        '
        for key in self.data:
            save_text += key + "," + str(self.data[key]) + '//'

        save_text = save_text[:-2]
        return save_text

    def get_from_line(self, line, account):
        # line = line.rstrip('\r\n')
        # line = re.sub('(?<=[A-Z])(,)(?=[A-Z\s])', ' ', line)
        # line = line.split(',')

        self.data['Account'] = account
        self.data['Actual'] = True

        for idx in range(len(self.config.app_dictionary['transaction_descriptors'][account])):

            transaction_descriptor = self.config.app_dictionary['transaction_descriptors'][account][idx]
            if line[idx] == '':
                line[idx] = '0.00'

            line[idx] = line[idx].rstrip('"')
            line[idx] = line[idx].lstrip('"')

            self.data[transaction_descriptor] = line[idx]

    def create_transaction(self):

        for key in self.data:

            self.data[key] = configuration.get_free_answer('Enter information to fill transaction field "{}": '.format(key))

    # def update_descriptor(self):
