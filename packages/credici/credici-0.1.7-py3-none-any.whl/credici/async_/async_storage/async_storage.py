from abc import abstractmethod
from uuid import UUID
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from credici.schema.storage_schema import StorageLedger, StorageUser, StorageUserCycle


class AsyncStorage:
    @abstractmethod
    async def add_transaction(
        self, user_id: UUID, amount: int, expire_at: datetime 
    ) -> None:
        pass

    @abstractmethod
    async def get_active_ledger(self, user_id: UUID) -> List[StorageLedger]:
        pass

    @abstractmethod
    async def get_all_user_transactions(self, user_id: UUID) -> List[StorageLedger]:
        pass

    @abstractmethod
    async def get_user_transactions_for_period(
        self, user_id: UUID, from_: datetime, to_: datetime
    ) -> List[StorageLedger]:
        pass

    @abstractmethod
    async def start_cycle(
        self, amount: int, time_delta: int, user_id: Optional[UUID | None] = None
    ) -> None:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> StorageUser:
        pass

    @abstractmethod
    async def commit_to_storage(self) -> None:
        pass

    @abstractmethod
    async def rollback_from_storage(self) -> None:
        pass

    @abstractmethod
    async def get_active_balance_grouped_by_expire_at(
        self, user_id: UUID
    ) -> List[StorageLedger]:
        pass