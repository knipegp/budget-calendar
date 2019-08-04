# TODO: add docstrings
# pylint: disable=missing-docstring
import os
import csv
import re
import shutil


# TODO: should this be more functional?
class Statement:  # pylint: disable=too-few-public-methods
    def __init__(self, file_path, account):
        self.data = dict()
        self._rows = list()
        self.file_path = file_path
        # self._check_file_path()
        self.account = account

    def _check_file_path(self):
        assert os.path.isfile(
            self.file_path
        ), "{} is not an existing " "statement file.".format(self.file_path)

    def _write(self, rows, header=("date", "description", "amount")):
        assert rows, "No valid rows read {}.".format(self.file_path)
        with open("temp.csv", "w") as csv_file:
            if not header:
                csv_writer = csv.writer(csv_file)
            else:
                csv_writer = csv.DictWriter(csv_file, header)
                csv_writer.writeheader()
            for row in rows:
                csv_writer.writerow(row)

        shutil.copyfile("temp.csv", self.file_path)

    def remove_file(self):
        os.remove(self.file_path)


# TODO: heavily object oriented approach is probably a bad choice
class WriteStatement(Statement):
    def write(self, rows, header=("date", "description", "amount")):
        self._write(rows, header)


class ReadStatement(Statement):
    def _read(self):
        self._prep_file()
        with open(self.file_path, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                self._rows.append(row)

    def _prep_file(self):
        start_read = False
        rows = list()
        with open(self.file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)

            # TODO: Discrepancy between reading new checkings and new credit
            try:
                for row in csv_reader:
                    if re.search("^date.*amount$", str(row).lower()):
                        break
                    elif re.search("date.*amount", str(row).lower()):
                        if not start_read:
                            start_read = True
                        else:
                            raise ValueError("Muliple headers read {}".format(row))

                    if start_read:
                        rows.append(row)

            except csv.Error as err:
                print(self.file_path)
                raise err

        if start_read:
            self._write(rows, None)

    def get_rows(self):
        if not self._rows:
            self._read()
        else:
            pass

        return self._rows