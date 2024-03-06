from datetime import datetime, timedelta
from uuid import UUID
from credici.schema.postgres_db_schema import DB_Ledger, DB_Users, DB_UserCycle
from sqlalchemy import func, select
from credici.exception import UserDoesNotExistError
from credici.async_.async_storage.async_storage import AsyncStorage
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import List, Optional
from sqlalchemy.dialects.postgresql import insert


class AsyncPostgresStorage(AsyncStorage):
    """
    The AsyncPostgresStorage class for managing transactions asynchronously.

    Attributes:
        url (str): The URL of the storage.
        auto_commit (bool): A flag to enable/disable auto-commit. If True, transactions are automatically committed.
            If False, users can manually manage transactions using the provided methods. The session starts when the class is instantiated.
    """

    url: str
    auto_commit: bool
    echo: bool

    def __init__(
        self, url: str, auto_commit: Optional[bool] = True, echo: Optional[bool] = False
    ):
        self.url = url
        self.engine = create_async_engine(url, echo=echo)
        self.auto_commit = auto_commit
        self._asession = None

        if self.auto_commit is False:
            self._asession = AsyncSession(self.engine)

    async def add_transaction(
        self, user_id: UUID, amount: int, expire_at: datetime
    ) -> None:
        """Adds a transaction to the storage asynchronously.

        Args:
            user_id (UUID): The unique identifier of the user.
            amount (int): The absolute amount of the credits.
            expire_at (datetime, optional): The time at which the credits will expire. Defaults to None.
        """
        if self.auto_commit is False:
            try:
                self._asession.add(
                    DB_Ledger(
                        user_id=user_id,
                        amount=amount,
                        created_at=datetime.utcnow(),
                        expire_at=expire_at,
                    )
                )
            except Exception:
                self._asession.rollback()
                raise
        else:
            async with AsyncSession(self.engine) as asession:
                try:
                    asession.execute(
                        insert(DB_Ledger).values(
                            user_id=user_id,
                            amount=amount,
                            created_at=datetime.utcnow(),
                            expire_at=expire_at,
                        )
                    )
                    await asession.commit()
                except Exception:
                    await asession.rollback()
                    raise

    async def get_user_transactions_for_period(
        self, user_id: UUID, from_: datetime, to_: datetime
    ) -> List[DB_Ledger]:
        """Get all transactions for a user within a given period asynchronously.

        Args:
            user_id (UUID): The unique identifier of the user.
            from_ (datetime): The start of the period.
            to_ (datetime): The end of the period.

        Returns:
            List[DB_Ledger]: A list of transactions for the user within the given period.
        """
        async with AsyncSession(self.engine) as asession:
            result = await asession.execute(
                select(DB_Ledger)
                .where(DB_Ledger.user_id == user_id)
                .where(DB_Ledger.created_at >= from_)
                .where(DB_Ledger.created_at <= to_)
            )
            return result.scalars().all()

    async def get_all_user_transactions(self, user_id: UUID) -> List[DB_Ledger]:
        """Get all transactions for a user asynchronously.

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            List[DB_Ledger]: A list of all transactions for the user.
        """
        async with AsyncSession(self.engine) as asession:
            try:
                result = await asession.execute(
                    select(DB_Ledger).where(DB_Ledger.user_id == user_id)
                )
                return result.scalars().all()
            except Exception:
                raise

    async def get_active_ledger(self, user_id: UUID) -> DB_Ledger:
        """Get the current active ledger for a user asynchronously.

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            DB_Ledger: The current active ledger for the user.
        """
        try:
            async with AsyncSession(self.engine) as asession:
                result = await asession.execute(
                    select(DB_Ledger)
                    .where(DB_Ledger.user_id == user_id)
                    .where(DB_Ledger.expire_at > datetime.utcnow())
                )
                return result.scalars().all()
        except Exception:
            raise

    async def get_active_balance_grouped_by_expire_at(
        self, user_id: UUID
    ) -> List[DB_Ledger]:
        """Get the current active ledger for a user grouped by expire_at asynchronously.

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            List[DB_Ledger]: The current active ledger for the user grouped by expire_at.
        """
        try:
            async with AsyncSession(self.engine) as asession:
                result = await asession.execute(
                    select(
                        DB_Ledger.expire_at,
                        func.sum(DB_Ledger.amount),
                    )
                    .where(DB_Ledger.user_id == user_id)
                    .where(DB_Ledger.expire_at > datetime.utcnow())
                    .group_by(DB_Ledger.expire_at)
                )
                return result.all()
        except Exception:
            raise

    async def get_active_balance(self, user_id: UUID) -> int | None:
        """Get the balance of a user asynchronously.

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            int: The balance of the user.
        """
        try:
            active_ledger = await self.get_active_ledger(user_id)
            if active_ledger is not None:
                for t in active_ledger:
                    active_balance = +t.amount
                return active_balance
            else:
                return None
        except Exception:
            raise

    async def start_cycle(
        self, amount: int, time_delta: int = 30, user_id: Optional[UUID | None] = None
    ) -> None:
        """Start a new cycle for a user asynchronously.

        Args:

            amount (int): The amount of credits to add to the user's balance.
            time_delta (int): The duration of the cycle in days. Defaults to 30.
            user_id (Optional[UUID], optional): The ID of the user. If None a new user will be created.
        """
        datetime_now = (
            datetime.utcnow()
        )  # we store the current date and time in a variable so it's the same across the function

        if user_id is None:
            async with AsyncSession(self.engine) as asession:
                try:
                    new_user_id = self._add_new_user()
                    asession.add(
                        DB_Ledger(
                            user_id=new_user_id,
                            amount=amount,
                            created_at=datetime_now,
                            expire_at=datetime_now.replace(
                                hour=23, minute=59, second=59
                            )
                            + timedelta(days=time_delta),
                        )
                    )
                    await asession.execute(
                        insert(DB_UserCycle).values(
                            user_id=new_user_id,
                            cycle_start_at=datetime_now,
                            cycle_end_at=datetime_now.replace(
                                hour=23, minute=59, second=59
                            )
                            + timedelta(days=time_delta),
                        )
                    )
                    await asession.commit()
                except Exception:
                    raise
        else:
            if self.get_user_by_id(user_id) is None:
                raise UserDoesNotExistError(user_id)
            async with AsyncSession(self.engine) as asession:
                try:
                    asession.add(
                        DB_Ledger(
                            user_id=user_id,
                            amount=amount,
                            created_at=datetime_now,
                            expire_at=datetime_now.replace(
                                hour=23, minute=59, second=59
                            )
                            + timedelta(days=time_delta),
                        )
                    )
                    await asession.execute(
                        insert(DB_UserCycle)
                        .values(
                            user_id=user_id,
                            cycle_start_at=datetime_now,
                            cycle_end_at=datetime_now.replace(
                                hour=23, minute=59, second=59
                            )
                            + timedelta(days=time_delta),
                        )
                        .on_conflict_do_update(
                            index_elements=["user_id"],
                            set_={
                                "cycle_start_at": datetime_now,
                                "cycle_end_at": datetime_now.replace(
                                    hour=23, minute=59, second=59
                                )
                                + timedelta(days=time_delta),
                            },
                        ),
                    )
                    await asession.commit()
                except Exception:
                    await asession.rollback()
                    raise

    async def _add_new_user(self) -> UUID:
        """Add a new user to the storage asynchronously.

        Returns:
            UUID: The unique identifier of the new user.
        """
        if self.auto_commit is False:
            try:
                new_user_id = await self._asession.execute(
                    insert(DB_Users).values().returning(DB_Users.id)
                )
                return new_user_id.scalar()
            except Exception:
                await self._asession.rollback()
                raise
        else:
            async with AsyncSession(self.engine) as asession:
                try:
                    new_user_id = await asession.execute(
                        insert(DB_Users).values().returning(DB_Users.id)
                    )
                    await asession.commit()
                    return new_user_id.scalar()
                except Exception:
                    await asession.rollback()
                    raise

    async def get_user_by_id(self, user_id: UUID) -> DB_Users:
        """Get a user by ID asynchronously.

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            DB_Users: The user object.
        """
        async with AsyncSession(self.engine) as asession:
            try:
                result = await asession.execute(
                    select(DB_Users).where(DB_Users.id == user_id)
                )
                return result.scalar_one_or_none()
            except Exception:
                raise

    async def commit_to_storage(self) -> None:
        """Commit changes to the storage layer if auto_commit=False."""
        if self.auto_commit is False:
            try:
                await self._asession.commit()
            except Exception:
                await self._asession.rollback()
                raise

    async def rollback_from_storage(self) -> None:
        """Rollback changes to the storage layer if auto_commit=False."""
        if self.auto_commit is False:
            try:
                await self._asession.rollback()
            except Exception:
                raise
            finally:
                await self._asession.close()
