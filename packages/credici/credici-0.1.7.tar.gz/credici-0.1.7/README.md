# Credici Library

The Credici library is a comprehensive solution designed for developers to manage credit-based subscriptions or pay-as-you-go systems efficiently. It provides a robust set of tools to handle user balances, transactions, and cycles with ease, both synchronously and asynchronously.

## Features

- **User Balance Management**: Track and manage the balance of users in your system.
- **Credit Transactions**: Add or subtract credits from a user's balance, with support for expiration dates.
- **Cycles**: Implement subscription cycles or billing periods, with the ability to start new cycles for users.
- **Transaction History**: Retrieve all transactions for a user, or transactions within a specific period.
- **Storage Flexibility**: Utilize the provided storage interface to integrate with your preferred storage solution.
- **Asynchronous Support**: Perform operations asynchronously for improved performance in I/O-bound applications.

## Getting Started

### Installation

To use the Credici library, first, ensure you have Python installed on your system. Then, install the library using pip or Poetry, depending on your project's setup.

#### Using pip

```bash
pip install credici
```

#### Using Poetry

```bash
poetry add credici
```


### Quick Start

After installing the Credici library, you can start using it by importing the necessary components and initializing them with your storage solution. Below are the steps to perform common actions:

#### Initialization

First, initialize the storage and create a `CrediciClient`:

```python
from credici.sync_.client.client import CrediciClient
from credici.storage.postgres_storage import PostgresStorage

# Initialize storage
storage = PostgresStorage('your_database_url')

# Create a CrediciClient
credici = CrediciClient(storage=storage)
```

#### Adding Credits to a User

To add credits to a user's account:

```python
# Add credits to a user
credici.add(user_id="user UUID", amount=100, expire_at=datetime(2025, 1, 1))
```
Credits can have an expiration date, enabling you to implement time-sensitive promotions or subscription models.

#### Subtracting Credits from a User

To subtract credits from a user's account:

```python
# Subtract credits from a user
credici.subtract(user_id="user UUID", amount=50)
```

#### Retrieving the Current Balance of a User

To retrieve the current balance of a user:

```python
# Retrieve the current balance of a user
balance = credici.get_balance(user_id="user UUID")
```

#### Starting a New Cycle for a User

The library supports various types of business models, such as subscription-based and pay-as-you-go systems. Here are examples for each:

##### Subscription Model
For a subscription model, where users are allocated a specific amount of credits at the beginning of each cycle:

```python
# Start a new cycle for a user with a specific amount of credits for a monthly subscription model
credici.start_cycle(amount=200, time_delta=30, user_id="user UUID")
```

##### Pay-As-You-Go Model
For a pay-as-you-go model, where users are only charged based on their usage you can simply start a new monthly cycle with 0 credits and add credits per use:
    
```python
credici.start_cycle(amount=0, time_delta=30, user_id="user UUID")
# To add credits per use, simply use the add method as needed:
credici.add(user_id="user UUID", amount=1)
```

#### Retrieving All Transactions for a User

To retrieve all transactions for a user:

```python
# Retrieve all transactions for a user
transactions = credici.get_all_user_transactions(user_id="user UUID")
for transaction in transactions:
    print(f"Transaction ID: {transaction.transaction_id}, Amount: {transaction.amount}")
```


## Contributing

We welcome contributions from the community! If you're interested in helping improve the Credici library, please check out our [contributing guidelines](#) for more information on how to get started.

## License

The Credici library is licensed under the MIT License. See the LICENSE file for more details.
```
