import os
import json


class AppConfiguration:

    def __init__(self, app_name, force_write=False):
        self.app_directory = os.path.dirname(os.path.realpath(__file__))
        self.config_directory = self.app_directory + '/.config'
        self.config_file = self.config_directory + '/{}.json'.format(str(app_name))

        self.config = {}

        if not os.path.exists(self.config_directory):
            os.makedirs(self.config_directory)

        if not os.path.isfile(self.config_file) or force_write:
            self.create_config(force_write)
            self.write_config()

        else:
            print "Application already configured"
            self.get_config()
            return

    # Create a configuration file to store the
    def create_config(self, force=False):

        if not os.path.exists(self.config_directory):
            os.makedirs(self.config_directory)

        elif os.path.isfile(self.config_file) and not force:
            print "Application already configured"
            return

        user_input = ' '
        self.config['accounts'] = list()
        while user_input:
            print 'Enter account identifier.'
            user_input = raw_input('Press return to quit: ')

            if user_input:
                self.config['accounts'].append(user_input)

            while not user_input:
                user_input = raw_input('Are {} correct? [y/n]: '.format(self.config['accounts']))

                if user_input in ['n', 'N']:
                    self.config['accounts'] = list()
                elif user_input not in ['n', 'N', 'y', 'Y']:
                    user_input = ''

            if user_input in ['y', 'Y']:
                break

    def write_config(self):

        with open(self.config_file, 'w') as config_json:
            json.dump(self.config, config_json)

    def get_config(self):

        with open(self.config_file) as config_json:
            self.config = json.load(config_json)
