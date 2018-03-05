import subprocess
import datetime
import re
import configuration


# Class for transactions read from bank statements
class Transaction:

    def __init__(self, transaction_cfg, line=None, new_transaction_info={}):
        self.transaction_info = new_transaction_info
        self.config = transaction_cfg

        if line and self.config['Account'] and not self.transaction_info:
            self.get_from_line(line, self.config['Account'])

        elif not self.transaction_info:
            self.transaction_info = self.create_future_transaction()

        else:
            print 'Transaction passed:'
            print 'Line: ' + str(line)
            print 'Account: ' + str(self.config['Account'])
            print 'New_transaction_info: ' + str(new_transaction_info)
            raise StandardError('Transaction not instantiated with valid information')

        date = self.transaction_info['Date']
        month, day, year = date.split('/')
        self.date = datetime.date(int(year), int(month), int(day))

    def print_transaction(self):
        save_text = '\n        '
        for key in self.transaction_info:
            save_text += key + "," + str(self.transaction_info[key]) + '//'

        save_text = save_text[:-2]
        return save_text

    def create_future_transaction(self):
        trans_dict = {}

        print 'Adding a future transaction'
        print 'Select an account for your new transaction:'


        return trans_dict

    def get_from_line(self, line, account):
        # line = line.rstrip('\r\n')
        # line = re.sub('(?<=[A-Z])(,)(?=[A-Z\s])', ' ', line)
        # line = line.split(',')

        self.transaction_info['Account'] = account
        self.transaction_info['Current'] = True

        for idx in range(len(self.config['info_dict_keys'])):

            if line[idx] == '':
                line[idx] = '0.00'

            line[idx] = line[idx].rstrip('"')
            line[idx] = line[idx].lstrip('"')

            self.transaction_info[self.config['info_dict_keys'][idx]] = line[idx]
