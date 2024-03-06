from datetime import datetime
from uuid import UUID
from credici.sync_.ledger import Ledger
from credici.sync_.storage.storage import Storage
from credici.exception import (
    UserDoesNotExistError,
)
from typing import Optional, Self
from pydantic import BaseModel, ConfigDict, Field


class Cycle(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: UUID = None
    user_id: UUID = None
    cycle_start_at: datetime = None
    cycle_end_at: datetime = None
    ledger: Ledger = None
    storage: Storage = Field(exclude=True)

    def start_cycle(
        self, amount: int, time_delta: int = 30, user_id: Optional[UUID | None] = None
    ):
        """Start a new cycle for a user.

        Args:
            amount (int): The amount of credits to add to the user's balance.
            time_delta (int): The duration of the cycle in days. Defaults to 30.
            user_id (Optional[UUID], optional): The ID of the user. If None a new user will be created.
        """
        self.storage.start_cycle(amount, time_delta, user_id)
