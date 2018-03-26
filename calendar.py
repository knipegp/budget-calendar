import datetime
import configuration
import jsonpickle


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
        prev_day_str = str(self.str_to_obj(day_str) - date_diff)

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

    def str_to_obj(self, date_str, delimeter='-'):
        year, month, day = date_str.split(delimeter)
        date_obj = datetime.date(int(year), int(month), int(day))
        return date_obj

    def print_calendar(self, output=True):

        for day in sorted(self.days):
            current_day_obj = self.days[day]
            current_day_obj.print_day()

    def save_calendar(self):
        file_name = self.config.app_directory + '/calendar_save.json'
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        json_str = jsonpickle.encode(self.days)

        with open(file_name, 'w') as json_file:
            json_file.write(json_str)


    # Update the running balance of each account of each day based on the
    # transactions added to each day of the calendar
    def update_running_bal(self):
        '''
        Update the running balances for all Day objects in the calendar.
        :return: 0 if the function executes without errors.
                 1 if the function executes with an error.
        '''

        for day in sorted(self.days):
            previous_day_obj = self.get_previous_day_obj(day)
            current_day_obj = self.days[day]
            current_day_obj.update_running_bal(previous_day_obj)