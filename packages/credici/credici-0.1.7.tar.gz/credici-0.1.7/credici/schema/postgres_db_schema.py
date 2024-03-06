from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from uuid import UUID


class Base(MappedAsDataclass, DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


class DB_Users(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )


class DB_UserCycle(Base):
    __tablename__ = "user_cycle"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    cycle_start_at: Mapped[datetime]
    cycle_end_at: Mapped[datetime]


class DB_Ledger(Base):
    __tablename__ = "ledger"

    transaction_id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[int]
    created_at: Mapped[datetime]  = mapped_column(server_default=text("now()"))
    expire_at: Mapped[datetime]
