from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class CreditTransaction(BaseModel):
    """
    Represents a ledger entry for a transaction.

    Attributes:
        transaction_id (UUID or None): The unique identifier of the transaction.
        user_id (UUID): The unique identifier of the user associated with the transaction.
        amount (int): The absolute amount of the transaction.
        created_at (datetime): The time at which the transaction was created.
        expire_at (datetime): The time at which the transaction will expire.
        
    """

    transaction_id: UUID 
    user_id: UUID
    amount: int
    created_at: datetime
    expire_at: datetime
