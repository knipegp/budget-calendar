import os
import csv
import re


class Statement(object):

    def __init__(self, filename, config, read=True):
        self.config = config
        self.data = dict()
        self.rows = list()
        self.filename = filename

        self._check_filename()
        self.account = self._get_account()
        if read:
            self.read()

    def _check_filename(self):
        abs_path = os.path.join(self.config.app_directory, 'transactions', self.filename)
        if os.path.isfile(self.filename):
            pass
        elif os.path.isfile(abs_path):
            self.filename = abs_path
        else:
            NotImplementedError('{} is not an existing statement file.'.format(self.filename))

    def _get_account(self):
        ret = None
        for account in self.config.accounts:

            if account in self.filename:
                ret = account

        if not ret:
            raise NotImplementedError('Cannot find valid account for {}'.format(self.filename))

        return ret

    def read(self):
        self.prep_file()
        with open(self.filename, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                self.rows.append(row)

    def prep_file(self):
        start_read = False
        rows = list()
        first_line = True
        with open(self.filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                if re.search('date.*amount', str(row).lower()):
                    if first_line:
                        break
                    elif not start_read:
                        start_read = True
                    else:
                        raise ValueError('Muliple headers read {}'.format(row))

                if start_read:
                    rows.append(row)

                first_line = False

        if start_read:
            self.write_statement(rows)

    def write_statement(self, rows):
        assert rows, 'No valid rows read {}.'.format(self.filename)
        with open(self.filename, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            for row in rows:
                csv_writer.writerow(row)

    def delete_file(self):
        os.remove(self.filename)
