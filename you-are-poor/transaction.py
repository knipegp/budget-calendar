"""Store a financial transaction"""
from datetime import date
from dataclasses import dataclass


@dataclass
class Transaction:
    """Minimal information describing a financial transaction

    currency_amount: currency exchanged as a result of the transaction
    exchange_date: the date on which the exchange took place
    id_description
    """
    # TODO: double-check docstring format
    amount: float
    execution_date: date
    id_description: str
