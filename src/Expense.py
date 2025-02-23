from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Expense:
    title: str
    description: str
    origin: str
    debit_amount_cents: int
    credit_amount_cents: int
    charge_posted_date: date
