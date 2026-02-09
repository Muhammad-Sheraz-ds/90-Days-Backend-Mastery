"""
Day 7 Exercise: Persistent Bank System with JSON

This file demonstrates:
- File handling with context managers
- JSON serialization/deserialization
- Saving and loading dataclass objects
- Error handling for file operations

Run this file to see persistence in action:
    python persistent_bank.py

Data will be saved to accounts.json.
"""

import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
from pathlib import Path
from enum import Enum


# ============================================================================
# 1. Configure Logging
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ============================================================================
# 2. Custom Exceptions
# ============================================================================

class BankError(Exception):
    """Base exception for banking errors."""
    pass


class InsufficientFundsError(BankError):
    """Raised when withdrawal exceeds balance."""
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Insufficient funds: balance ${balance:.2f}, need ${amount:.2f}")


class NegativeAmountError(BankError):
    """Raised when amount is negative."""
    def __init__(self, amount: float):
        super().__init__(f"Amount cannot be negative: ${amount:.2f}")


class AccountNotFoundError(BankError):
    """Raised when account doesn't exist."""
    def __init__(self, account_id: str):
        super().__init__(f"Account not found: {account_id}")


# ============================================================================
# 3. Transaction Type Enum
# ============================================================================

class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"


# ============================================================================
# 4. Transaction Dataclass
# ============================================================================

@dataclass
class Transaction:
    """Represents a bank transaction."""
    id: str
    type: TransactionType
    amount: float
    balance_after: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    description: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return {
            "id": self.id,
            "type": self.type.value,  # Convert enum to string
            "amount": self.amount,
            "balance_after": self.balance_after,
            "timestamp": self.timestamp,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Create Transaction from dict."""
        return cls(
            id=data["id"],
            type=TransactionType(data["type"]),
            amount=data["amount"],
            balance_after=data["balance_after"],
            timestamp=data["timestamp"],
            description=data.get("description")
        )


# ============================================================================
# 5. BankAccount Dataclass with JSON Persistence
# ============================================================================

@dataclass
class BankAccount:
    """Bank account with JSON persistence."""
    account_id: str
    owner: str
    balance: float = 0.0
    transactions: list[Transaction] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    _transaction_counter: int = field(default=0, repr=False)
    
    def _generate_transaction_id(self) -> str:
        self._transaction_counter += 1
        return f"{self.account_id}-TXN-{self._transaction_counter:04d}"
    
    def deposit(self, amount: float, description: Optional[str] = None) -> Transaction:
        """Deposit money into account."""
        if amount <= 0:
            raise NegativeAmountError(amount)
        
        self.balance += amount
        txn = Transaction(
            id=self._generate_transaction_id(),
            type=TransactionType.DEPOSIT,
            amount=amount,
            balance_after=self.balance,
            description=description
        )
        self.transactions.append(txn)
        logger.info(f"Deposited ${amount:.2f} to {self.account_id} (balance: ${self.balance:.2f})")
        return txn
    
    def withdraw(self, amount: float, description: Optional[str] = None) -> Transaction:
        """Withdraw money from account."""
        if amount <= 0:
            raise NegativeAmountError(amount)
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        
        self.balance -= amount
        txn = Transaction(
            id=self._generate_transaction_id(),
            type=TransactionType.WITHDRAWAL,
            amount=amount,
            balance_after=self.balance,
            description=description
        )
        self.transactions.append(txn)
        logger.info(f"Withdrew ${amount:.2f} from {self.account_id} (balance: ${self.balance:.2f})")
        return txn
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return {
            "account_id": self.account_id,
            "owner": self.owner,
            "balance": self.balance,
            "transactions": [t.to_dict() for t in self.transactions],
            "created_at": self.created_at,
            "_transaction_counter": self._transaction_counter
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "BankAccount":
        """Create BankAccount from dict."""
        account = cls(
            account_id=data["account_id"],
            owner=data["owner"],
            balance=data["balance"],
            transactions=[Transaction.from_dict(t) for t in data["transactions"]],
            created_at=data["created_at"]
        )
        account._transaction_counter = data.get("_transaction_counter", len(account.transactions))
        return account


# ============================================================================
# 6. AccountManager with JSON File Persistence
# ============================================================================

@dataclass
class AccountManager:
    """Manages accounts with JSON persistence."""
    accounts: dict[str, BankAccount] = field(default_factory=dict)
    data_file: Path = field(default=Path("accounts.json"))
    
    _account_counter: int = field(default=0, repr=False)
    
    def __post_init__(self):
        """Load existing data on initialization."""
        if self.data_file.exists():
            self.load_from_file()
    
    def _generate_account_id(self) -> str:
        self._account_counter += 1
        return f"ACC-{self._account_counter:06d}"
    
    def create_account(self, owner: str, initial_deposit: float = 0.0) -> BankAccount:
        """Create a new account and save."""
        if initial_deposit < 0:
            raise NegativeAmountError(initial_deposit)
        
        account_id = self._generate_account_id()
        account = BankAccount(
            account_id=account_id,
            owner=owner,
            balance=initial_deposit
        )
        
        if initial_deposit > 0:
            account.transactions.append(Transaction(
                id=f"{account_id}-TXN-0000",
                type=TransactionType.DEPOSIT,
                amount=initial_deposit,
                balance_after=initial_deposit,
                description="Initial deposit"
            ))
        
        self.accounts[account_id] = account
        self.save_to_file()  # Auto-save
        
        logger.info(f"Created account {account_id} for {owner}")
        return account
    
    def get_account(self, account_id: str) -> BankAccount:
        """Get account by ID."""
        account = self.accounts.get(account_id)
        if account is None:
            raise AccountNotFoundError(account_id)
        return account
    
    def deposit(self, account_id: str, amount: float, description: str = None) -> Transaction:
        """Deposit and save."""
        account = self.get_account(account_id)
        txn = account.deposit(amount, description)
        self.save_to_file()
        return txn
    
    def withdraw(self, account_id: str, amount: float, description: str = None) -> Transaction:
        """Withdraw and save."""
        account = self.get_account(account_id)
        txn = account.withdraw(amount, description)
        self.save_to_file()
        return txn
    
    # ========================================================================
    # JSON Persistence Methods
    # ========================================================================
    
    def save_to_file(self) -> None:
        """Save all accounts to JSON file."""
        data = {
            "accounts": {aid: acc.to_dict() for aid, acc in self.accounts.items()},
            "_account_counter": self._account_counter
        }
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.debug(f"Saved {len(self.accounts)} accounts to {self.data_file}")
        except IOError as e:
            logger.error(f"Failed to save data: {e}")
            raise
    
    def load_from_file(self) -> None:
        """Load accounts from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.accounts = {
                aid: BankAccount.from_dict(acc_data) 
                for aid, acc_data in data.get("accounts", {}).items()
            }
            self._account_counter = data.get("_account_counter", len(self.accounts))
            
            logger.info(f"Loaded {len(self.accounts)} accounts from {self.data_file}")
        except FileNotFoundError:
            logger.info(f"No existing data file found at {self.data_file}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {self.data_file}: {e}")
            raise
    
    def get_summary(self) -> str:
        """Get summary of all accounts."""
        lines = ["=" * 50, "ACCOUNT SUMMARY", "=" * 50]
        for aid, acc in self.accounts.items():
            lines.append(f"{aid}: {acc.owner} - ${acc.balance:.2f}")
        lines.append(f"\nTotal accounts: {len(self.accounts)}")
        return "\n".join(lines)


# ============================================================================
# 7. Demo
# ============================================================================

def demo():
    """Demonstrate persistence."""
    print("\n" + "=" * 60)
    print("DAY 7: Persistent Bank System Demo")
    print("=" * 60)
    
    # Initialize manager (loads existing data if any)
    manager = AccountManager()
    
    # Check if we have existing data
    if manager.accounts:
        print("\n✓ Loaded existing accounts from file!")
        print(manager.get_summary())
    else:
        print("\n→ No existing data, creating new accounts...")
        
        # Create accounts
        alice = manager.create_account("Alice", 1000.0)
        bob = manager.create_account("Bob", 500.0)
        
        # Perform transactions
        manager.deposit(alice.account_id, 250.0, "Bonus")
        manager.withdraw(alice.account_id, 100.0, "Groceries")
        
        print(manager.get_summary())
    
    # Show persistence proof
    print("\n" + "-" * 60)
    print("Data saved to: accounts.json")
    print("Run this script again to see data persistence!")
    print("-" * 60)
    
    # Show file contents
    if Path("accounts.json").exists():
        print("\nFile contents (first 500 chars):")
        content = Path("accounts.json").read_text()
        print(content[:500] + "..." if len(content) > 500 else content)


def test_error_handling():
    """Test file error handling."""
    print("\n" + "=" * 60)
    print("Error Handling Tests")
    print("=" * 60)
    
    manager = AccountManager()
    
    # Create test account
    if not manager.accounts:
        acc = manager.create_account("Test User", 100.0)
    else:
        acc = list(manager.accounts.values())[0]
    
    # Test 1: Insufficient funds
    print("\n[Test 1] Attempting to withdraw more than balance...")
    try:
        manager.withdraw(acc.account_id, 10000.0)
    except InsufficientFundsError as e:
        print(f"  ✓ Caught: {e}")
    
    # Test 2: Account not found
    print("\n[Test 2] Attempting to access non-existent account...")
    try:
        manager.get_account("INVALID-123")
    except AccountNotFoundError as e:
        print(f"  ✓ Caught: {e}")
    
    print("\n✓ All error cases handled!")


if __name__ == "__main__":
    demo()
    test_error_handling()
