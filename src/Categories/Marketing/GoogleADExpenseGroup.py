from re import compile
from AbstractExpenseGroup import ExpenseGroup


class GoogleAdExpenseGroup(ExpenseGroup):
    def __init__(self):
        supplier_name = "Google ADs"
        description = "Money spent on Google advertising"
        match_rules = [compile(r"^GOOGLE\*ADS.*")]
        super().__init__(supplier_name, description, match_rules)
