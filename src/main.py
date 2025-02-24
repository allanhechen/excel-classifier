from datetime import date
from openpyxl import Workbook
from AbstractCategory import Category
from Categories.Blocked._BlockedCategory import BlockedCategory
from Categories.CatchAll._CatchAllCategory import CatchAllCategory
from Categories.Marketing._MarketingCategory import MarketingCategory
from Categories.MealEntertainment._MealEntertainmentCategory import (
    MealEntertainmentCategory,
)
from CategoryManager import CategoryManager
from InputWorkbook import InputWorkbook

if __name__ == "__main__":
    filename = input("Input file name: ")
    expenses = InputWorkbook.read_workbook(filename)

    categories: set[Category] = set([MarketingCategory(), MealEntertainmentCategory()])
    blocked_category = BlockedCategory()
    catch_all_category = CatchAllCategory()

    category_manager = CategoryManager(categories, blocked_category, catch_all_category)

    for expense in expenses:
        category_manager.test_expense(expense)

    output_workbook = Workbook()
    february = date(date.today().year, 2, 1)
    category_manager.fill_workbook(output_workbook, february)
