from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID
from sqlalchemy import create_engine, select, update, func
from sqlalchemy.orm import Session
from credici.exception import InsufficientFundsError, UserDoesNotExistError
from credici.sync_.storage.storage import Storage
from credici.schema.postgres_db_schema import DB_Ledger
from credici.schema.postgres_db_schema import DB_UserCycle
from credici.schema.postgres_db_schema import DB_Users
from sqlalchemy.dialects.postgresql import insert


class PostgresStorage(Storage):
    """
    The PostgresStorage class for managing transactions.

    Attributes:
        url (str): The URL of the storage.
        auto_commit (bool): A flag to enable/disable auto-commit. If True, transactions are automatically committed.
            If False, users can manually manage transactions using the provided methods. The session starts when the class is instantiated.

    """

    url: str
    auto_commit: bool = True

    def __init__(self, url: str, auto_commit: Optional[bool] = True):
        self.url = url
        self.engine = create_engine(self.url)
        self.auto_commit = auto_commit
        self._session = None

        if self.auto_commit is False:
            self._session = Session(self.engine)

    def add_transaction(self, user_id: UUID, amount: int, expire_at: datetime) -> None:
        """
        Adds a transaction to the storage.

        Args:
            user_id (UUID): The unique identifier of the user.
            amount (int): The absolute amount of the transaction.
        """
        if self.auto_commit is False:
            try:
                self._session.add(
                    DB_Ledger(
                        user_id=user_id,
                        amount=amount,
                        created_at=datetime.utcnow(),
                        expire_at=expire_at,
                    )
                )
            except Exception:
                self._session.rollback()
                raise
        else:
            with Session(self.engine) as session:
                try:
                    session.execute(
                        insert(DB_Ledger).values(
                            user_id=user_id,
                            amount=amount,
                            created_at=datetime.utcnow(),
                            expire_at=expire_at,
                        )
                    )
                    session.commit()
                except Exception:
                    session.rollback()
                    raise

    def get_active_ledger(self, user_id: UUID) -> DB_Ledger:
        with Session(self.engine) as session:
            try:
                stmt = (
                    select(DB_Ledger)
                    .where(DB_Ledger.user_id == user_id)
                    .where(DB_Ledger.expire_at > datetime.utcnow())
                    .order_by(DB_Ledger.created_at.desc())
                )
                q = session.execute(stmt)
                if len(q) > 0:
                    return q.scalars().all()
                else:
                    return False
            except Exception:
                raise

    def get_active_balance_grouped_by_expire_at(self, user_id: UUID) -> List[DB_Ledger]:
        """Get the current active ledger for a user grouped by expire_at.

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            List[DB_Ledger]: The current active ledger for the user grouped by expire_at.
        """
        try:
            with Session(self.engine) as asession:
                result = asession.execute(
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

    def get_all_user_transactions(self, user_id: UUID) -> List[DB_Ledger]:
        """
        Retrieves all the transactions for a specific user.
        """
        with Session(self.engine) as session:
            try:
                stmt = (
                    select(DB_Ledger)
                    .where(DB_Ledger.user_id == user_id)
                    .order_by(DB_Ledger.created_at.desc())
                )
                q = session.execute(stmt)
                return q.scalars().all()
            except Exception:
                raise

    def get_user_transactions_for_period(
        self, user_id: UUID, from_: datetime, to_: datetime
    ) -> None:
        """
        Retrieves the transactions for a specific user within a given period.
        """
        with Session(self.engine) as session:
            try:
                stmt = (
                    select(DB_Ledger)
                    .where(DB_Ledger.user_id == user_id)
                    .where(DB_Ledger.created_at >= from_)
                    .where(DB_Ledger.created_at <= to_)
                    .order_by(DB_Ledger.created_at.desc())
                )
                q = session.execute(stmt)
                return q.scalars().all()
            except Exception:
                raise

    def start_cycle(
        self, amount: int, time_delta: int, user_id: Optional[UUID] = None
    ) -> None:
        """
        Starts a new cycle for a user whether it exists or not.

        Args:
            amount (int): The amount of the transaction.
            time_delta (int): The duration of the transaction in days.
            user_id (Optional[UUID], optional): The ID of the user. Defaults to None.

        """
        datetime_now = (
            datetime.utcnow()
        )  # we store the current date and time in a variable so it's the same across the function
        if user_id is None:
            with Session(self.engine) as session:
                try:
                    new_user_id = self._add_new_user()
                    session.execute(
                        insert(DB_Ledger).values(
                            user_id=new_user_id,
                            amount=amount,
                            created_at=datetime_now,
                            expire_at=datetime_now.replace(
                                hour=23, minute=59, second=59
                            )
                            + timedelta(days=time_delta),
                        )
                    )
                    session.execute(
                        insert(DB_UserCycle).values(
                            user_id=new_user_id,
                            cycle_start_at=datetime_now,
                            cycle_end_at=datetime_now.replace(
                                hour=23, minute=59, second=59
                            )
                            + timedelta(days=time_delta),
                        )
                    )
                    session.commit()
                except Exception:
                    session.rollback()
                    raise
        else:
            if self.get_user_by_id(user_id) is None:
                raise UserDoesNotExistError(user_id)

            with Session(self.engine) as session:
                try:
                    session.execute(
                        insert(DB_Ledger).values(
                            user_id=user_id,
                            amount=amount,
                            created_at=datetime_now,
                            expire_at=datetime_now.replace(
                                hour=23, minute=59, second=59
                            )
                            + timedelta(days=time_delta),
                        )
                    )
                    session.execute(
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
                    session.commit()
                except Exception:
                    session.rollback()
                    raise

    def _get_cycle(self, user_id: UUID) -> DB_UserCycle | None:
        with Session(self.engine) as session:
            try:
                stmt = select(DB_UserCycle).where(DB_UserCycle.user_id == user_id)
                result = session.execute(stmt)
                return result.scalar_one_or_none()
            except Exception:
                raise

    def _add_new_user(self):
        if self.auto_commit is False:
            try:
                stmt = insert(DB_Users).values().returning(DB_Users.id)
                new_user_id = self._session.execute(stmt).scalar()
                return new_user_id
            except Exception:
                self._session.rollback()
                raise
        else:
            with Session(self.engine) as session:
                try:
                    stmt = insert(DB_Users).values().returning(DB_Users.id)
                    new_user_id = session.execute(stmt).scalar()
                    session.commit()
                    return new_user_id
                except Exception:
                    session.rollback()
                    raise

    def get_user_by_id(self, user_id: UUID) -> DB_Users | None:
        """
        Retrieves a user by its ID."""
        with Session(self.engine) as session:
            try:
                stmt = select(DB_Users).where(DB_Users.id == user_id)
                result = session.execute(stmt)
                return result.scalar_one_or_none()
            except Exception:
                raise

    def commit_to_storage(self) -> None:
        """
        Commit the current session to the storage.
        """
        if self.auto_commit is False:
            try:
                self._session.commit()
            except Exception:
                self._session.rollback()
                raise
            finally:
                self._session.close()

    def rollback_from_storage(self) -> None:
        """
        Rollback the current session from the storage.
        """
        if self.auto_commit is False:
            try:
                self._session.rollback()
            except Exception:
                raise
            finally:
                self._session.close()
