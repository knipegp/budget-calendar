import datetime
import configuration
import jsonpickle
import os
import csv
import transaction
import day
from matplotlib import pyplot as py


# A calendar which stores Day objects and maintains the relationship of
# balances between each day
class Calendar(object):

    def __init__(self, app_name='calendar_application'):
        # Key: date     Value: Day objectround
        self.days = {}
        self.first_day = None
        self.last_day = None
        self.application_name = app_name
        self.config = configuration.AppConfiguration(self.application_name)

    def get_previous_day_obj(self, day_str):
        ''' Get the previous day for the given day_str.

        :param day_str: Date key to reference Day object in self.days.
        :return: A Day obj for the previous day to the day_str. None
                 if previous day does not exist in dictionary.
        '''

        date_diff = datetime.timedelta(days=1)
        prev_day_str = str(configuration.str_to_obj(day_str) - date_diff)

        if prev_day_str not in self.days:
            prev_day_str = None

            for day in sorted(self.days):

                if day >= day_str:
                    break

                prev_day_str = day

        if prev_day_str:
            prev_day_obj = self.days[prev_day_str]
        else:
            prev_day_obj = None

        return prev_day_obj



    def print_calendar(self, output=True):
        for day in sorted(self.days):
            current_day_obj = self.days[day]
            print current_day_obj

    def save_calendar(self):
        file_name = self.config.app_directory + '/calendar_save.json'
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        json_str = jsonpickle.encode(self.days)

        with open(file_name, 'w') as json_file:
            json_file.write(json_str)


    # Update the running balance of each account of each day based on the
    # transactions added to each day of the calendar
    def update_running_bal(self):
        """
        Update the running balances for all Day objects in the calendar.
        :return: 0 if the function executes without errors.
                 1 if the function executes with an error.
        """

        for day_str in sorted(self.days):
            previous_day_obj = self.get_previous_day_obj(day_str)
            current_day_obj = self.days[day_str]
            current_day_obj.update_running_bal(previous_day_obj)

    # Retrieve all new transactions from files in the given directory. Return a
    # list of transaction objects
    def open_transactions(self):
        transactions_list = list()
        transaction_dir = self.config.app_directory + '/transactions'
        files_in_dir = os.listdir(transaction_dir)

        for transaction_file_name in files_in_dir:
            transactions_list += self.read_new_csv(transaction_file_name)

        if transactions_list:
            self.update_cal(transactions_list)

    # TODO: Should the header be stored in the configuration file?
    # Should each file check that it matches the known header?
    #
    def read_new_csv(self, csv_file_name):
        start_read = False
        header = list()
        new_transactions_list = list()

        with open(csv_file_name, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            file_account = None
            for account in self.config.app_dictionary['accounts']:

                if account in csv_file_name:
                    file_account = account

            if not file_account:
                raise NotImplementedError('{} not valid account.'.format(file_account))

            for row in csvreader:
                transaction_data = {}

                if not start_read and len(row) > 3:
                    header = row
                    start_read = True

                elif header:

                    for idx, key in enumerate(header):
                        # TODO: This should live in add_standard_keys
                        if not row[idx]:
                            transaction_data[key] = '0.00'
                        else:
                            transaction_data[key] = row[idx]

                    transaction_data = self.add_standard_keys(file_account, transaction_data)
                    new_transaction = transaction.Transaction(file_account, transaction_data)
                    new_transactions_list.append(new_transaction)

        return new_transactions_list

    def add_standard_keys(self, account, transaction_dict):

        for key in transaction_dict:
            if 'Date' in key:
                new_date = transaction_dict.pop(key)
                new_date_obj = configuration.correct_date(new_date)
                transaction_dict['Date'] = new_date_obj.isoformat()
                break

        transaction_dict['Account'] = account

        return transaction_dict

    # Add transactions to the calendar and update the necessary values
    def update_cal(self, transactions_list):
        # Need to account for when only 1 transaction is passed
        if type(transactions_list) is not list: transactions_list = [transactions_list]

        for transaction in transactions_list:

            if str(transaction.date) not in self.days:
                self.days[str(transaction.date)] = day.Day(transaction.date)

            self.days[str(transaction.date)].add_transaction(transaction)

        self.update_running_bal()
        self.config.write_config()

    # def save_to_csv(self):
    #     config_directory = self.config.config_directory
    #     # Check to see if save files exist create them if they don't
    #     for account in self.config.app_dictionary['accounts']:
    #         file_name = os.path.join(config_directory, 'save_calendar_{}.csv'.format(account))
    #         if not os.path.isfile(file_name):
    #             # TODO: Add headers to configuration dictionary
    #             header = self.config.app_dictionary['']
    #             with open(file_name, 'w') as csvfile:
    #                 csvwriter = csv.writer(csvfile)
    #                 csvwriter.write()
    #
    #     for current_day in self.days:
    #
    #         with open('calendar_save_{}.csv'.format(account), 'a') as csvfile,
    #              open():



