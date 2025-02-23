from abc import ABC, abstractmethod
from datetime import date

from AbstractExpenseGroup import ExpenseGroup
from Expense import Expense


class Category(ABC):
    def __init__(self, name: str, expense_groups: set[ExpenseGroup]):
        self._name = name
        self._expense_groups = expense_groups

    def test_expense(self, expense: Expense) -> bool:
        for expense_group in self._expense_groups:
            if expense_group.test_expense(expense):
                return True

        return False

    def get_expenses(
        self, starting_date: date, ending_date: date
    ) -> dict[str, set[Expense]]:
        results: dict[str, set[Expense]] = {}

        for expense_group in self._expense_groups:
            expense_group_expenses = expense_group.get_expenses(
                starting_date, ending_date
            )
            results[expense_group.get_supplier_name()] = expense_group_expenses

        return results

    def get_name(self) -> str:
        return self._name
