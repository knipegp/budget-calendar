import datetime
import os
import utils


# A calendar which stores Day objects and maintains the relationship of
# balances between each day
class Calendar(object):

    def __init__(self, config):
        # Key: date     Value: Day objectround
        self.days = {}
        self.first_day = None
        self.last_day = None
        self.config = config

    # def get_previous_day_obj(self, day_str):
    #     ''' Get the previous day for the given day_str.
    #
    #     :param day_str: Date key to reference Day object in self.days.
    #     :return: A Day obj for the previous day to the day_str. None
    #              if previous day does not exist in dictionary.
    #     '''
    #
    #     date_diff = datetime.timedelta(days=1)
    #     prev_day_str = str(configuration.str_to_obj(day_str) - date_diff)
    #
    #     if prev_day_str not in self.days:
    #         prev_day_str = None
    #
    #         for day in sorted(self.days):
    #
    #             if day >= day_str:
    #                 break
    #
    #             prev_day_str = day
    #
    #     if prev_day_str:
    #         prev_day_obj = self.days[prev_day_str]
    #     else:
    #         prev_day_obj = None
    #
    #     return prev_day_obj

    def print_calendar(self, output=True):
        for day in sorted(self.days):
            current_day_obj = self.days[day]
            print current_day_obj

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
            transaction_file_name = os.path.join(transaction_dir, transaction_file_name)
            transactions_list += self.read_new_csv(transaction_file_name)

        if transactions_list:
            self.update_cal(transactions_list)

    # Add transactions to the calendar and update the necessary values
    def update(self, transactions_list):
        # Need to account for when only 1 transaction is passed
        if type(transactions_list) is not list: transactions_list = [transactions_list]

        for transaction in transactions_list:

            if str(transaction.date) not in self.days:
                self.days[str(transaction.date)] = day.Day(transaction.date)

            self.days[str(transaction.date)].add_transaction(transaction)

        self.update_running_bal()
        self.config.write_config()
