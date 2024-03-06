from datetime import datetime
from uuid import UUID
from credici.sync_.credit_transaction import CreditTransaction
from credici.sync_.ledger import Ledger
from credici.sync_.cycle import Cycle
from credici.sync_.storage.storage import Storage
from typing import List, Optional


class CrediciClient:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.cycle = Cycle(storage=self.storage)
        self.ledger = Ledger(storage=self.storage)

    def add(self, user_id: UUID, amount: int, expire_days: int = 30) -> None:
        """Add credits to a user.

        Args:
            user_id (UUID): The unique identifier of the user.
            amount (int): The absolute amount of credits to add.
            expire_days (int): The number of days until the credits expire.
        """
        return self.ledger.add(user_id, amount, expire_days)

    def subtract(self, user_id: UUID, amount: int) -> None:
        """Subtract credits from a user.

        Args:
            user_id (UUID): The unique identifier of the user.
            amount (int): The absolute amount of credits to subtract.
        """
        return self.ledger.subtract(user_id, amount)

    def get_balance(self, user_id: UUID) -> int:
        """Get the balance of a user.

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            UserBalance: The user balance object of the given user.
        """
        return self.ledger.get_active_balance(user_id)

    def start_cycle(
        self, amount: int, time_delta: int = 30, user_id: Optional[UUID | None] = None
    ) -> None:
        """Start a new cycle for a user.

        Args:

            amount (int): The amount of credits to add to the user's balance.
            time_delta (int): The duration of the cycle in days. Defaults to 30.
            user_id (Optional[UUID], optional): The ID of the user. If None a new user will be created.
        """
        return self.cycle.start_cycle(amount, time_delta, user_id)

    def get_user_transactions_for_period(
        self, user_id: UUID, from_: datetime, to_: datetime
    ) -> List[CreditTransaction]:
        """Get all transactions for a user within a given period.

        Args:
            user_id (UUID): The unique identifier of the user.
            from_ (datetime): The start of the period.
            to_ (datetime): The end of the period.
        """
        return self.ledger.get_user_transactions_for_period(user_id, from_, to_)

    def get_all_user_transactions(self, user_id: UUID) -> List[CreditTransaction]:
        """Get all transactions for a user.

        Args:
            user_id (UUID): The unique identifier of the user.
        """
        return self.ledger.get_all_user_transactions(user_id)

    def commit_to_storage(self) -> None:
        """Commit changes to the storage layer if auto_commit=False."""
        return self.storage.commit_to_storage()

    def rollback_from_storage(self) -> None:
        """Rollback changes to the storage layer if auto_commit=False."""
        return self.storage.rollback_from_storage()
