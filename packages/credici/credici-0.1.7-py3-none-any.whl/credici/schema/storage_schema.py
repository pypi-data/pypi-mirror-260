from uuid import UUID
from datetime import datetime

"""Base schema for the storage layer."""


class StorageUser:
    id: UUID


class StorageUserCycle:
    id: UUID
    user_id: UUID
    cycle_start_at: datetime
    cycle_end_at: datetime


class StorageLedger:
    transaction_id: UUID
    user_id: UUID
    amount: int
    created_at: datetime
    expire_at: datetime
