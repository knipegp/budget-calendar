import os
import utils
import json


class AppConfiguration(object):

    def __init__(self, app_name, force_write=False):
        self.app_directory = os.path.dirname(os.path.realpath(__file__))
        self.config_directory = os.path.join(self.app_directory, '.config')
        self.transaction_directory = os.path.join(self.app_directory, 'transactions', 'new')
        self.saved_transaction_directory = os.path.join(self.app_directory, 'transactions', 'saved')
        # TODO: switch config file to toml
        self.config_file = self.config_directory + '/{}.json'.format(str(app_name))

        # self.transaction_descriptors = dict()
        self.accounts = list()
        self.starting_bal = dict()

        if not os.path.exists(self.config_directory):
            os.makedirs(self.config_directory)

        if not os.path.isfile(self.config_file) or force_write:
            self.create_config(force_write)
            self.write_config()

        else:
            self.get_config()
            return

    # Create a configuration file to store the
    def create_config(self, force=False):

        if not os.path.exists(self.config_directory):
            os.makedirs(self.config_directory)

        elif os.path.isfile(self.config_file) and not force:
            print "Application already configured"
            return

        self.accounts = utils.get_free_answer('Enter account identifier: ', 0)
        for account in self.accounts:
            self.starting_bal[account] = float(utils.get_free_answer('Enter starting balance for account {}: '.format(account)))

    def write_config(self):
        write_dict = {
            'accounts': self.accounts,
            'starting_bal': self.starting_bal
        }

        with open(self.config_file, 'w') as config_json:
            json.dump(write_dict, config_json, indent=4, sort_keys=True)

    def get_config(self):
        with open(self.config_file) as config_json:
            decoded = json.load(config_json)

        self.accounts = decoded['accounts']
        self.starting_bal = decoded['starting_bal']

    def add_account(self, account):

        # default_descriptors = ['Name', 'Description', 'Amount']
        self.accounts.append(account)

        # print 'Default transaction descriptors: {}'.format(default_descriptors)
        # ans = utils.get_binary_answer('Use default transaction descriptors for account {}?'.format(account))

        # if not ans:
        #     ans = utils.get_free_answer('Enter account transaction descriptor: '.format(default_descriptors), 0)
        #     self.transaction_descriptors[account] = ans
        # else:
        #     self.transaction_descriptors[account] = default_descriptors
