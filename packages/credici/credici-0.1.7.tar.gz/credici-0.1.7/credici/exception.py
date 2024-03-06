from datetime import datetime
from uuid import UUID


class InsufficientFundsError(Exception):
    amount: int
    user_id: UUID

    def __init__(self, user_id: UUID, amount: int):
        self.amount = amount
        self.user_id = user_id

        super().__init__(
            f"User {user_id} does not have enough funds to subtract {amount}."
        )


class AmountNegativeError(Exception):
    amount: int

    def __init__(self, amount: int):
        self.amount = amount
        super().__init__(f"Amount {amount} is negative. Provide a positive amount.")


class UserDoesNotExistError(Exception):
    user_id: UUID

    def __init__(self, user_id: UUID):
        self.user_id = user_id
        super().__init__(f"User {user_id} does not exist.")


class CreditExpiredError(Exception):
    user_id: UUID
    date: datetime

    def __init__(self, user_id: UUID, date: datetime):
        self.user_id = user_id
        self.date = date
        super().__init__(f"User {user_id} credit has expired on {date}")
