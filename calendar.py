import datetime
import logging
import configuration
import jsonpickle
# TODO: Budget calendar needs to go
import budget_calendar


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

    def str_to_obj(self, date_str, delimeter='-'):
        year, month, day = date_str.split(delimeter)
        date_obj = datetime.date(int(year), int(month), int(day))
        return date_obj

    def print_calendar(self, output=True):
        date_diff = datetime.timedelta(days=1)
        curr_day = self.first_day
        save_text = ''

        while curr_day <= self.last_day:
            save_text += self.days[curr_day].print_date()
            date_obj = self.str_to_obj(curr_day)
            curr_day = str(date_obj + date_diff)

        if output:
            print save_text
        return save_text

    # Write the calendar and all contents to a single file
    # TODO: Should this change to a json?
    # Or the entire calendar could be written to csv form and each account could have its own csv?
    def save_calendar(self):
        calendar_save = open(self.config.app_directory + '/calendar_save.txt', 'w')

        calendar_text = self.print_calendar(output=False)
        calendar_save.write(calendar_text)
        calendar_save.close()

    def complete_calendar(self):
        self.first_day = min(self.days)
        year, month, day = self.first_day.split('-')
        temp_date = datetime.date(int(year), int(month), 1)
        self.first_day = str(temp_date)

        self.last_day = max(self.days)
        year, month, day = self.last_day.split('-')
        month = int(month) + 1
        day = 1

        if month == 13:
            month = 1
            year = int(year) + 1

        date_diff = datetime.timedelta(days=1)
        temp_date = datetime.date(int(year), int(month), int(day))

        self.last_day = str(temp_date - date_diff)

        curr_date = self.first_day

        while curr_date <= self.last_day:

            if curr_date not in self.days:
                year, month, day = curr_date.split('-')
                # TODO: Budget day needs to go
                self.days[curr_date] = budget_calendar.BudgetDay(datetime.date(int(year), int(month), int(day)))

            year, month, day = curr_date.split('-')
            temp_date = datetime.date(int(year), int(month), int(day))
            curr_date = str(temp_date + date_diff)


# An object that stores a list of transaction objects
class Day(object):

    def __init__(self, date):
        self.date = date

    def print_date(self):
        save_text = ''
        save_text += '\nDate,' + str(self.date)

        # TODO: The account, daily total, running total string needs to go away to make this module portable to
        # other apps
        for key in self.account_totals:
            save_text += "\n    Account,{}//Daily Total,{}//Running Total,{}".format(key,
                                                                      self.account_totals[key],
                                                                      self.account_running_bal[key])

            if key in self.account_trans:

                for transaction in self.account_trans[key]:
                    save_text += transaction.print_transaction()

        return save_text
