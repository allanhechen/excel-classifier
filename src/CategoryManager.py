from copy import deepcopy
from datetime import date, timedelta
from openpyxl import Workbook, worksheet
from openpyxl.worksheet.worksheet import Worksheet
from AbstractCategory import Category
from Expense import Expense


class CategoryManager:
    def __init__(
        self,
        categories: set[Category],
        blocked_category: Category,
        catch_all_category: Category,
        concerned_date: date,
    ):
        self._categories = categories
        self._blocked_category = blocked_category
        self._catch_all_category = catch_all_category
        self._date_ranges = CategoryManager.find_date_ranges(concerned_date)

    def test_expense(self, expense: Expense):
        if self._blocked_category.test_expense(expense):
            return

        for category in self._categories:
            if category.test_expense(expense):
                return

        self._catch_all_category.test_expense(expense)

    def fill_workbook(self, workbook: Workbook):
        all_categories = list(self._categories)
        all_categories.append(self._catch_all_category)
        all_categories.append(self._blocked_category)

        for category in all_categories:
            self._fill_category(workbook, category)

    def _fill_category(self, workbook: Workbook, category: Category):
        worksheet: Worksheet = workbook.create_sheet(category.get_name())
        expense_groups = category.get_expense_groups()

        worksheet["A2"] = "Supplier"
        worksheet["B2"] = "Description"

        for col_offset, date_range in enumerate(self._date_ranges, 2):
            col = CategoryManager.get_col_index(col_offset)
            [_, ending_date] = date_range
            worksheet[col + "2"] = "Amount"
            worksheet[col + "1"] = f"Week of {ending_date.strftime('%b %d')}"

        for offset, expense_group in enumerate(expense_groups, 2):
            row = CategoryManager.get_row_index(offset)

            worksheet["A" + row] = expense_group.get_supplier_name()
            worksheet["B" + row] = expense_group.get_description()

            for col_offset, [starting_date, ending_date] in enumerate(
                self._date_ranges, 2
            ):
                col = CategoryManager.get_col_index(col_offset)
                relevant_expenses = expense_group.get_expenses(
                    starting_date, ending_date
                )
                total_expenses = 0
                for expense in relevant_expenses:
                    total_expenses += expense.debit_amount_cents

                worksheet[col + row] = total_expenses / 100

        # C column + length + 1 blank
        final_col = 1 + len(self._date_ranges)
        final_col_index = CategoryManager.get_col_index(final_col)
        total_col_index = CategoryManager.get_col_index(final_col + 2)

        worksheet[total_col_index + "1"] = "Total"
        worksheet[total_col_index + "2"] = "Amount"

        for row_offset in range(len(expense_groups)):
            row = CategoryManager.get_row_index(row_offset + 2)
            worksheet[total_col_index + row] = f"=SUM(C{row}:{final_col_index+ row})"

        CategoryManager.adjust_col_size(worksheet)

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

    @staticmethod
    def get_col_index(offset: int):
        return chr(ord("A") + offset)

    @staticmethod
    def get_row_index(offset: int):
        return chr(ord("1") + offset)

    @staticmethod
    def adjust_col_size(worksheet: Worksheet):
        for col in worksheet.columns:
            max_length = 0
            col_letter = col[0].column_letter  # type: ignore
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass

            worksheet.column_dimensions[col_letter].width = max_length + 2
