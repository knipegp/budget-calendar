import configuration
from calendar import Calendar


def main():
    cal = Calendar()
    cal.open_transactions()
    cal.print_calendar()
    # cal.save_calendar()
    # cal.days['2018-02-08'].print_date()


if __name__ == "__main__":
    main()