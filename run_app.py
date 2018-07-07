import budget_calendar


if __name__ == '__main__':
    cal = budget_calendar.Calendar()
    cal.open_transactions()
    cal.print_calendar()
