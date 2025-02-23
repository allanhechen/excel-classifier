from re import compile
from AbstractExpenseGroup import ExpenseGroup


class NotServiceChargeableExpenseGroup(ExpenseGroup):
    def __init__(self):
        supplier_name = "Blocked"
        description = "Not Service Chargeable"
        match_rules = [compile(r"^Not Service Chargeable.*")]
        super().__init__(supplier_name, description, match_rules)
