"""
Day 5 Exercise: Typed Models with Dataclasses

This file contains the exercise solution for Day 5 of Backend Mastery.
Topics covered:
- Converting classes to dataclasses
- Adding type hints
- Using field() for advanced configurations
- Creating typed methods

Run mypy validation:
    mypy typed_models.py
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


# ============================================================================
# 1. Transaction Type Enum
# ============================================================================

class TransactionType(Enum):
    """Enum for transaction types."""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"


# ============================================================================
# 2. Transaction Dataclass
# ============================================================================

@dataclass
class Transaction:
    """
    Represents a bank transaction.
    
    Attributes:
        id: Unique transaction identifier
        amount: Transaction amount (positive value)
        type: Type of transaction (deposit, withdrawal, transfer)
        timestamp: When the transaction occurred (auto-generated)
    """
    id: str
    amount: float
    type: TransactionType
    timestamp: datetime = field(default_factory=datetime.now)
    description: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate transaction data after initialization."""
        if self.amount <= 0:
            raise ValueError("Transaction amount must be positive")


# ============================================================================
# 3. BankAccount Dataclass
# ============================================================================

@dataclass
class BankAccount:
    """
    Represents a bank account with transaction history.
    
    Attributes:
        account_id: Unique account identifier
        owner: Account owner's name
        balance: Current account balance
        transactions: List of account transactions
    """
    account_id: str
    owner: str
    balance: float = 0.0
    transactions: list[Transaction] = field(default_factory=list)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    def deposit(self, amount: float, description: Optional[str] = None) -> Transaction:
        """
        Deposit money into the account.
        
        Args:
            amount: Amount to deposit (must be positive)
            description: Optional transaction description
            
        Returns:
            The created Transaction object
            
        Raises:
            ValueError: If amount is not positive or account is inactive
        """
        if not self.is_active:
            raise ValueError("Cannot deposit to inactive account")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        transaction = Transaction(
            id=f"TXN-{len(self.transactions) + 1:04d}",
            amount=amount,
            type=TransactionType.DEPOSIT,
            description=description
        )
        self.transactions.append(transaction)
        return transaction

    def withdraw(self, amount: float, description: Optional[str] = None) -> Transaction:
        """
        Withdraw money from the account.
        
        Args:
            amount: Amount to withdraw (must be positive)
            description: Optional transaction description
            
        Returns:
            The created Transaction object
            
        Raises:
            ValueError: If amount is invalid or insufficient funds
        """
        if not self.is_active:
            raise ValueError("Cannot withdraw from inactive account")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        
        self.balance -= amount
        transaction = Transaction(
            id=f"TXN-{len(self.transactions) + 1:04d}",
            amount=amount,
            type=TransactionType.WITHDRAWAL,
            description=description
        )
        self.transactions.append(transaction)
        return transaction

    def get_transaction_history(self) -> list[Transaction]:
        """Return a copy of the transaction history."""
        return self.transactions.copy()


# ============================================================================
# 4. AccountManager with Typed Methods
# ============================================================================

@dataclass
class AccountManager:
    """
    Manages multiple bank accounts.
    
    Provides methods for creating accounts and transferring funds.
    """
    accounts: dict[str, BankAccount] = field(default_factory=dict)
    
    def create_account(self, owner: str, initial_deposit: float = 0.0) -> BankAccount:
        """
        Create a new bank account.
        
        Args:
            owner: Name of the account owner
            initial_deposit: Optional initial deposit amount
            
        Returns:
            The newly created BankAccount
        """
        account_id = f"ACC-{len(self.accounts) + 1:06d}"
        account = BankAccount(
            account_id=account_id,
            owner=owner,
            balance=initial_deposit
        )
        
        if initial_deposit > 0:
            account.transactions.append(Transaction(
                id=f"TXN-0001",
                amount=initial_deposit,
                type=TransactionType.DEPOSIT,
                description="Initial deposit"
            ))
        
        self.accounts[account_id] = account
        return account

    def get_account(self, account_id: str) -> Optional[BankAccount]:
        """
        Retrieve an account by ID.
        
        Args:
            account_id: The account identifier
            
        Returns:
            The BankAccount if found, None otherwise
        """
        return self.accounts.get(account_id)

    def transfer(
        self, 
        from_account_id: str, 
        to_account_id: str, 
        amount: float
    ) -> tuple[Transaction, Transaction]:
        """
        Transfer funds between accounts.
        
        Args:
            from_account_id: Source account ID
            to_account_id: Destination account ID
            amount: Amount to transfer
            
        Returns:
            Tuple of (withdrawal_transaction, deposit_transaction)
            
        Raises:
            ValueError: If accounts not found or transfer fails
        """
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)
        
        if from_account is None:
            raise ValueError(f"Source account {from_account_id} not found")
        if to_account is None:
            raise ValueError(f"Destination account {to_account_id} not found")
        
        withdrawal = from_account.withdraw(
            amount, 
            description=f"Transfer to {to_account_id}"
        )
        deposit = to_account.deposit(
            amount, 
            description=f"Transfer from {from_account_id}"
        )
        
        return withdrawal, deposit

    def get_total_balance(self) -> float:
        """Calculate total balance across all active accounts."""
        return sum(
            acc.balance for acc in self.accounts.values() 
            if acc.is_active
        )


# ============================================================================
# 5. Demo / Test Code
# ============================================================================

def main() -> None:
    """Demonstrate the typed models."""
    # Create account manager
    manager = AccountManager()
    
    # Create accounts
    alice_account = manager.create_account("Alice", initial_deposit=1000.0)
    bob_account = manager.create_account("Bob", initial_deposit=500.0)
    
    print(f"Created account for Alice: {alice_account}")
    print(f"Created account for Bob: {bob_account}")
    
    # Perform transactions
    alice_account.deposit(250.0, "Salary bonus")
    alice_account.withdraw(100.0, "Groceries")
    
    # Transfer between accounts
    manager.transfer(
        alice_account.account_id, 
        bob_account.account_id, 
        200.0
    )
    
    # Display results
    print(f"\nAlice's balance: ${alice_account.balance:.2f}")
    print(f"Bob's balance: ${bob_account.balance:.2f}")
    print(f"Total managed balance: ${manager.get_total_balance():.2f}")
    
    # Show transaction history
    print(f"\nAlice's transactions:")
    for txn in alice_account.get_transaction_history():
        print(f"  {txn.id}: {txn.type.value} ${txn.amount:.2f} - {txn.description or 'N/A'}")


if __name__ == "__main__":
    main()
