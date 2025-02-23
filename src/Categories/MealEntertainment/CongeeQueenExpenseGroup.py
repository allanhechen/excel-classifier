from re import compile
from AbstractExpenseGroup import ExpenseGroup


class CongeeQueenExpenseGroup(ExpenseGroup):
    def __init__(self):
        supplier_name = "Congee Queen"
        description = "Money spent at Congee Queen"
        match_rules = [compile(r"^CONGEE QUEEN.*")]
        super().__init__(supplier_name, description, match_rules)
