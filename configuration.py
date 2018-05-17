import os
import json
import csv
import datetime


class AppConfiguration:

    def __init__(self, app_name, force_write=False):
        self.app_directory = os.path.dirname(os.path.realpath(__file__))
        self.config_directory = self.app_directory + '/.config'
        self.config_file = self.config_directory + '/{}.json'.format(str(app_name))

        self.app_dictionary = dict()
        self.app_dictionary['transaction_descriptors'] = {}

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

        self.app_dictionary['accounts'] = get_free_answer('Enter account identifier: ', 0)

    def write_config(self):

        with open(self.config_file, 'w') as config_json:
            json.dump(self.app_dictionary, config_json)

    def get_config(self):

        with open(self.config_file) as config_json:
            self.app_dictionary.update(json.load(config_json))

    def add_account(self, account):

        default_descriptors = ['Name', 'Description', 'Amount']
        self.app_dictionary['accounts'].append(account)

        print 'Default transaction descriptors: {}'.format(default_descriptors)
        ans = get_binary_answer('Use default transaction descriptors for account {}?'.format(account))

        if not ans:
            ans = get_free_answer('Enter account transaction descriptor: '.format(default_descriptors), 0)
            self.app_dictionary['transaction_descriptors'][account] = ans
        else:
            self.app_dictionary['transaction_descriptors'][account] = default_descriptors


def get_free_answer(prompt, responses=1, possible_responses=list()):
    ret = list()
    loop = False
    question = 0

    if responses < 1:
        print 'Hit return when all responses have been entered.'
        loop = True
        responses = 1

    while question < responses:
        response = raw_input(prompt)
        ret.append(response)

        # Need to make this a regular expression match to be more flexible
        while possible_responses and response not in possible_responses:
            response = raw_input(prompt)

        if loop and response:
            question = 0

        elif not response and loop:
            ret = ret[:-1]

            ans = get_binary_answer('Is {} correct?'.format(ret))

            if ans:
                break
            else:
                ret = list()

        elif responses == 1:
            ret = response

    return ret


def get_binary_answer(prompt):
    ans = ' '
    possible_ans = ['y', 'Y', 'n', 'N']

    while ans not in possible_ans:
        ans = raw_input(prompt + ' [y,n]: ')

    if ans in ['y', 'Y']:
        ret = True

    else:
        ret = False

    return ret


# def get_csv_dict_reader(self, file_name, keys=list(), keyword='date'):
#     account = None
#     begin_read = False
#
#     for iden in self.config.app_dictionary['accounts']:
#
#         if iden in file_name:
#             account = iden
#             break
#
#     if not account:
#         raise ValueError('Filename does not match a known account')
#
#     with open(file_name, 'rb') as csvfile:
#
#         if account not in self.config.app_dictionary['transaction_descriptors']:
#             csv_reader = csv.reader(csvfile)
#
#             for row in csv_reader:
#
#                 if 'Date' in row:
#
#         csv_reader = csv.DictReader(csvfile, self.config.app_dictionary['transaction_descriptors'][account])


def get_csv_keys(file_name, keyword):
    keys = None

    with open(file_name, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:

            for element in row:

                if keyword.lower() in element.lower():
                    keys = row
                    break

            if keys:
                break

    if not keys:
        raise Exception('Could not find keys for {}'.format(file_name))

    return keys


def str_to_obj(date_str, delimeter='-'):
    year, month, day = date_str.split(delimeter)
    date_obj = datetime.date(int(year), int(month), int(day))
    return date_obj


def correct_date(date_str):
    month, day, year = date_str.split('/')
    date_obj = datetime.date(int(year), int(month), int(day))
    return date_obj


if __name__ == '__main__':
    print get_free_answer('Tell ME! ', 0)
