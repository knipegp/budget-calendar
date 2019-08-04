# TODO: write docstrings
# pylint: disable=missing-docstring

# TODO: this should probably be functional
class Menu:  # pylint: disable=too-few-public-methods
    def __init__(self, cal):
        print("Welcome to the budget-calendar app!")

        self.options = {
            "Print calendar.": cal.print_calendar,
            "Add transaction": {""},
            "Delete transaction": {},
        }
