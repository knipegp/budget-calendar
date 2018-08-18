import csv
import datetime


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
        question += 1

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
    try:
        month, day, year = date_str.split('/')
    except:
        pass
    date_obj = datetime.date(int(year), int(month), int(day))
    return date_obj