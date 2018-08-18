
class Menu:

    def __init__(self, cal):
        print 'Welcome to the budget-calendar app!'

        self.options = {'Print calendar.':
                            cal.print_calendar,
                        'Add transaction':
                            {''},
                        'Delete transaction':
                            {}}