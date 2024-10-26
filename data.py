import openpyxl
import pytest

# """
class Data:
    file = 'data.xlsx'
    success = []
    failed = []

    @classmethod
    def load_data(cls, sheet):
        workbook = openpyxl.load_workbook(cls.file)
        worksheet = workbook[sheet]

        cls.success.clear()
        for v in worksheet.iter_rows(values_only=True):
            Data.success.append(v)


def get_data(sheet):
    Data.load_data(sheet)
    return Data.success


# """

