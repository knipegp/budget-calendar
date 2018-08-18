import datetime
import os
import utils


# A calendar which stores Day objects and maintains the relationship of
# balances between each day
class Calendar(object):

    def __init__(self, config):
        self.days = {}
        self.first_day = None
        self.last_day = None
        self.config = config

    def set_calendar_range(self, first_day, last_day):
        self.first_day = first_day
        self.last_day = last_day
