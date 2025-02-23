from re import compile
from AbstractExpenseGroup import ExpenseGroup


class UberExpenseGroup(ExpenseGroup):
    def __init__(self):
        supplier_name = "Uber"
        description = "Money spent on Uber Rides"
        match_rules = [compile(r"^UBER.*")]
        super().__init__(supplier_name, description, match_rules)
