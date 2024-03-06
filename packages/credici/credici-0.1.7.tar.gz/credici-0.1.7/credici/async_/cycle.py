from datetime import datetime
from uuid import UUID
from credici.async_.ledger import AsyncLedger
from credici.async_.async_storage.async_storage import AsyncStorage
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class AsyncCycle(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: UUID = None
    user_id: UUID = None
    cycle_start_at: datetime = None
    cycle_end_at: datetime = None
    ledger: AsyncLedger = None
    storage: AsyncStorage = Field(exclude=True)

    async def start_cycle(
        self, amount: int, time_delta: int = 30, user_id: Optional[UUID | None] = None
    ):
        """Start a new cycle for a user asynchronously.

        Args:
            amount (int): The amount of credits to add to the user's balance.
            time_delta (int): The duration of the cycle in days. Defaults to 30.
            user_id (Optional[UUID], optional): The ID of the user. If None a new user will be created.
        """
        await self.storage.start_cycle(amount, time_delta, user_id)
