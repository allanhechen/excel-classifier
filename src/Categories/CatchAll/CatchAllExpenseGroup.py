from re import compile
from AbstractExpenseGroup import ExpenseGroup


class CatchAllExpenseGroup(ExpenseGroup):
    def __init__(self):
        supplier_name = "CatchAll"
        description = "Items that do not fit into any other group"
        match_rules = [compile(r".*")]
        super().__init__(supplier_name, description, match_rules)
