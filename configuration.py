import os
import subprocess
import re
import transaction


class AppConfiguration:

    def __init__(self, app_name, force_write=False):
        self.app_dir = os.path.dirname(os.path.realpath(__file__))
        self.trans_iden = {}
        self.config_dir = self.app_dir + '/.config'
        self.config_file = self.config_dir + '/{}.conf'.format(str(app_name))
        self.acc_num = 0
        self.acc_iden = None
        self.acc_trans_descriptors = {}

        if not os.path.exists(self.config_dir) or force_write:
            os.makedirs(self.config_dir)
            self.create_config(force_write)

        elif os.path.isfile(self.config_file):
            print "Application already configured"
            self.read_config_file()
            return

    # Create a configuration file to store the
    def create_config(self, force=False):
        config = {}

        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        elif os.path.isfile(self.config_file) and not force:
            print "Application already configured"
            return

        config['num'] = raw_input('Number of accounts: ')

        for idx in range(int(config['num'])):
            config['id' + str(idx)] = raw_input('Enter account identifier {}: '.format(str(idx)))

        open_file = open(self.config_file, 'w')

        for key in config:
            open_file.write('{} {}\n'.format(key, config[key]))

        open_file.close()

    def read_config_file(self):
        config = {}
        ids = list()

        with open(self.config_file, 'r') as conf_file:

            for line in conf_file:
                line = line.split()
                config[line[0]] = line[1]

        for idx in range(int(config['num'])):
            ids.append(config['id'+str(idx)])

        self.acc_iden = ids