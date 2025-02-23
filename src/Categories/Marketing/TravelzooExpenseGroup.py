from re import compile
from AbstractExpenseGroup import ExpenseGroup


class TravelzooExpenseGroup(ExpenseGroup):
    def __init__(self):
        supplier_name = "Travelzoo"
        description = "Money spent on Travelzoo advertising"
        match_rules = [compile(r".*TRAVELZOO INC WW.*")]
        super().__init__(supplier_name, description, match_rules)
