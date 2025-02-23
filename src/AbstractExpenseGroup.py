from abc import ABC, abstractmethod
from datetime import date
import re

from Expense import Expense


class ExpenseGroup(ABC):
    def __init__(
        self, supplier_name: str, description: str, match_rules: list[re.Pattern]
    ):
        self._supplier_name = supplier_name
        self._description = description
        self._match_rules = match_rules
        self._expenses: set[Expense] = set()

    def test_expense(self, expense: Expense) -> bool:
        for rule in self._match_rules:
            if re.fullmatch(rule, expense.title):
                self._expenses.add(expense)
                return True
        return False

    def get_expenses(self, starting_date: date, ending_date: date) -> set[Expense]:
        results: set[Expense] = set()

        for expense in self._expenses:
            if (
                starting_date <= expense.charge_posted_date
                and expense.charge_posted_date <= ending_date
            ):
                results.add(expense)

        return results

    def get_supplier_name(self):
        return self._supplier_name
