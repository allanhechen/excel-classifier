from copy import deepcopy
from datetime import date, timedelta
from openpyxl import Workbook
from AbstractCategory import Category
from Expense import Expense


class CategoryManager:
    def __init__(
        self,
        categories: set[Category],
        blocked_category: Category,
        catch_all_category: Category,
    ):
        self._categories = categories
        self._blocked_category = blocked_category
        self._catch_all_category = catch_all_category

    def test_expense(self, expense: Expense):
        if self._blocked_category.test_expense(expense):
            return

        for category in self._categories:
            if category.test_expense(expense):
                return

        self._catch_all_category.test_expense(expense)

    def fill_workbook(self, workbook: Workbook, concerned_date: date):
        all_categories = list(self._categories)
        all_categories.append(self._catch_all_category)
        all_categories.append(self._blocked_category)

        for category in all_categories:
            CategoryManager._fill_category(workbook, category, concerned_date)

    @staticmethod
    def _fill_category(workbook: Workbook, category: Category, concerned_date: date):
        workbook.create_sheet(category._name)
        date_ranges = CategoryManager.find_date_ranges(concerned_date)

        for [starting_date, ending_date] in date_ranges:
            month_expenses = category.get_expenses(starting_date, ending_date)
            # TODO: actually derive a way to write categories into their own sheets
            print(month_expenses)

    @staticmethod
    def find_date_ranges(concerned_date: date) -> list[list[date]]:
        result: list[list[date]] = []
        starting_month = concerned_date.month

        current_day = deepcopy(concerned_date)
        range_start_date = deepcopy(concerned_date)

        # find the first Friday
        while current_day.weekday() != 4:
            current_day += timedelta(days=1)
        result.append([range_start_date, deepcopy(current_day)])

        # increments days until we hit the next month
        while True:
            range_start_date = current_day + timedelta(days=1)
            current_day += timedelta(days=7)
            if current_day.month != starting_month:
                break

            range_end_date = deepcopy(current_day)
            result.append([range_start_date, range_end_date])

        # edge case: last day of the month was a Friday
        if range_start_date.month != starting_month:
            return result

        # walk back until we hit the last day of the month
        while current_day.month != starting_month:
            current_day -= timedelta(days=1)

        result.append([range_start_date, current_day])

        return result
