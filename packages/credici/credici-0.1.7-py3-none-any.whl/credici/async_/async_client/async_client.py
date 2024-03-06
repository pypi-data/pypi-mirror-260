from datetime import datetime
from uuid import UUID
from credici.async_.async_storage.async_storage import AsyncStorage
from credici.async_.ledger import AsyncLedger
from credici.async_.cycle import AsyncCycle
from typing import List, Optional
from credici.sync_.credit_transaction import CreditTransaction


class AsyncCrediciClient:
    def __init__(self, storage: AsyncStorage):
        self.storage = storage
        self.cycle = AsyncCycle(storage=self.storage)
        self.ledger = AsyncLedger(storage=self.storage)

    async def add(self, user_id: UUID, amount: int, expire_days: int = 30) -> None:
        """Add credits to a user asynchronously.

        Args:
            user_id (UUID): The unique identifier of the user.
            amount (int): The absolute amount of credits to add.
            expire_at (datetime): The time at which the credits will expire. Defaults to 30 days.
        """
        await self.ledger.add(user_id, amount, expire_days)

    async def subtract(self, user_id: UUID, amount: int) -> None:
        """Subtract credits from a user asynchronously.

        Args:
            user_id (UUID): The unique identifier of the user.
            amount (int): The absolute amount of credits to subtract.
        """
        await self.ledger.subtract(user_id, amount)

    async def get_active_balance(self, user_id: UUID) -> int:
        """Get the balance of a user asynchronously.

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            AsyncUserBalance: The user balance object of the given user.
        """
        return await self.ledger.get_active_balance(user_id)

    async def start_cycle(
        self, amount: int, time_delta: int = 30, user_id: Optional[UUID | None] = None
    ) -> None:
        """Start a new cycle for a user asynchronously.

        Args:
            amount (int): The amount of credits to add to the user's balance.
            time_delta (int): The duration of the cycle in days. Defaults to 30.
            user_id (Optional[UUID], optional): The ID of the user. If None, a new user will be created.
        """
        await self.cycle.start_cycle(amount, time_delta, user_id)

    async def get_user_transactions_for_period(
        self, user_id: UUID, from_: datetime, to_: datetime
    ) -> List[CreditTransaction]:
        """Get all transactions for a user within a given period asynchronously.

        Args:
            user_id (UUID): The unique identifier of the user.
            from_ (datetime): The start of the period.
            to_ (datetime): The end of the period.
        """
        return await self.ledger.get_user_transactions_for_period(user_id, from_, to_)

    async def get_all_user_transactions(self, user_id: UUID) -> List[CreditTransaction]:
        """Get all transactions for a user asynchronously.

        Args:
            user_id (UUID): The unique identifier of the user.
        """
        return await self.ledger.get_all_user_transactions(user_id)

    async def commit_to_storage(self) -> None:
        """Commit changes to the storage layer asynchronously if auto_commit=False."""
        await self.storage.commit_to_storage()

    async def rollback_from_storage(self) -> None:
        """Rollback changes to the storage layer asynchronously if auto_commit=False."""
        await self.storage.rollback_from_storage()
