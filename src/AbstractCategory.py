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

    def get_expense_groups(self) -> set[ExpenseGroup]:
        return self._expense_groups

    def get_name(self) -> str:
        return self._name
