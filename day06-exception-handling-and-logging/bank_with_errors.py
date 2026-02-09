"""
Day 6 Exercise: Bank System with Exception Handling & Logging

This file demonstrates:
- Custom exceptions (InsufficientFundsError, NegativeAmountError)
- try/except/finally blocks for safe operations
- Logging to both console and file
- Proper error handling patterns

Run this file to see logging in action:
    python bank_with_errors.py

Check bank.log for file output.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


# ============================================================================
# 1. Configure Logging (Console + File)
# ============================================================================

def setup_logging() -> logging.Logger:
    """Configure logging to both console and file."""
    logger = logging.getLogger("bank")
    logger.setLevel(logging.DEBUG)
    
    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Console handler - INFO level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    console_handler.setFormatter(console_format)
    
    # File handler - DEBUG level (more detail)
    file_handler = logging.FileHandler('bank.log', mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


logger = setup_logging()


# ============================================================================
# 2. Custom Exceptions
# ============================================================================

class BankError(Exception):
    """Base exception for all banking errors."""
    pass


class InsufficientFundsError(BankError):
    """Raised when withdrawal amount exceeds available balance."""
    
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        self.shortfall = amount - balance
        super().__init__(
            f"Insufficient funds: balance ${balance:.2f}, "
            f"attempted ${amount:.2f}, short ${self.shortfall:.2f}"
        )


class NegativeAmountError(BankError):
    """Raised when a negative amount is provided."""
    
    def __init__(self, amount: float, operation: str = "transaction"):
        self.amount = amount
        self.operation = operation
        super().__init__(
            f"Invalid {operation}: amount cannot be negative (${amount:.2f})"
        )


class AccountNotFoundError(BankError):
    """Raised when account doesn't exist."""
    
    def __init__(self, account_id: str):
        self.account_id = account_id
        super().__init__(f"Account not found: {account_id}")


class AccountInactiveError(BankError):
    """Raised when operating on an inactive account."""
    
    def __init__(self, account_id: str):
        self.account_id = account_id
        super().__init__(f"Account is inactive: {account_id}")


# ============================================================================
# 3. Transaction Type Enum
# ============================================================================

class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"


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
    timestamp: datetime = field(default_factory=datetime.now)
    description: Optional[str] = None
    success: bool = True


# ============================================================================
# 5. BankAccount with Exception Handling
# ============================================================================

@dataclass
class BankAccount:
    """Bank account with proper exception handling and logging."""
    account_id: str
    owner: str
    balance: float = 0.0
    is_active: bool = True
    transactions: list[Transaction] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    _transaction_counter: int = field(default=0, repr=False)
    
    def _generate_transaction_id(self) -> str:
        """Generate unique transaction ID."""
        self._transaction_counter += 1
        return f"{self.account_id}-TXN-{self._transaction_counter:04d}"
    
    def _validate_active(self) -> None:
        """Check if account is active."""
        if not self.is_active:
            raise AccountInactiveError(self.account_id)
    
    def _validate_amount(self, amount: float, operation: str) -> None:
        """Validate amount is positive."""
        if amount <= 0:
            raise NegativeAmountError(amount, operation)
    
    def deposit(self, amount: float, description: Optional[str] = None) -> Transaction:
        """
        Deposit money into the account.
        
        Args:
            amount: Amount to deposit (must be positive)
            description: Optional transaction description
            
        Returns:
            Transaction record
            
        Raises:
            AccountInactiveError: If account is inactive
            NegativeAmountError: If amount is not positive
        """
        logger.debug(f"Deposit attempt: account={self.account_id}, amount=${amount:.2f}")
        
        try:
            self._validate_active()
            self._validate_amount(amount, "deposit")
            
            self.balance += amount
            
            transaction = Transaction(
                id=self._generate_transaction_id(),
                type=TransactionType.DEPOSIT,
                amount=amount,
                balance_after=self.balance,
                description=description
            )
            self.transactions.append(transaction)
            
            logger.info(
                f"Deposit successful: account={self.account_id}, "
                f"amount=${amount:.2f}, new_balance=${self.balance:.2f}"
            )
            return transaction
            
        except BankError as e:
            logger.error(f"Deposit failed: {e}")
            raise
    
    def withdraw(self, amount: float, description: Optional[str] = None) -> Transaction:
        """
        Withdraw money from the account.
        
        Args:
            amount: Amount to withdraw (must be positive and <= balance)
            description: Optional transaction description
            
        Returns:
            Transaction record
            
        Raises:
            AccountInactiveError: If account is inactive
            NegativeAmountError: If amount is not positive
            InsufficientFundsError: If balance is too low
        """
        logger.debug(
            f"Withdrawal attempt: account={self.account_id}, "
            f"amount=${amount:.2f}, balance=${self.balance:.2f}"
        )
        
        try:
            self._validate_active()
            self._validate_amount(amount, "withdrawal")
            
            if amount > self.balance:
                raise InsufficientFundsError(self.balance, amount)
            
            self.balance -= amount
            
            transaction = Transaction(
                id=self._generate_transaction_id(),
                type=TransactionType.WITHDRAWAL,
                amount=amount,
                balance_after=self.balance,
                description=description
            )
            self.transactions.append(transaction)
            
            logger.info(
                f"Withdrawal successful: account={self.account_id}, "
                f"amount=${amount:.2f}, new_balance=${self.balance:.2f}"
            )
            return transaction
            
        except BankError as e:
            logger.error(f"Withdrawal failed: {e}")
            raise
    
    def get_statement(self) -> str:
        """Generate account statement."""
        lines = [
            f"Account Statement: {self.account_id}",
            f"Owner: {self.owner}",
            f"Current Balance: ${self.balance:.2f}",
            f"Status: {'Active' if self.is_active else 'Inactive'}",
            "-" * 60,
            "Transactions:"
        ]
        
        for txn in self.transactions[-10:]:  # Last 10 transactions
            lines.append(
                f"  {txn.timestamp:%Y-%m-%d %H:%M} | {txn.type.value:10} | "
                f"${txn.amount:>10.2f} | Balance: ${txn.balance_after:>10.2f}"
            )
        
        return "\n".join(lines)


# ============================================================================
# 6. AccountManager with Exception Handling
# ============================================================================

@dataclass
class AccountManager:
    """Manages multiple accounts with proper exception handling."""
    accounts: dict[str, BankAccount] = field(default_factory=dict)
    
    _account_counter: int = field(default=0, repr=False)
    
    def _generate_account_id(self) -> str:
        """Generate unique account ID."""
        self._account_counter += 1
        return f"ACC-{self._account_counter:06d}"
    
    def create_account(
        self, 
        owner: str, 
        initial_deposit: float = 0.0
    ) -> BankAccount:
        """
        Create a new bank account.
        
        Args:
            owner: Account owner's name
            initial_deposit: Optional initial deposit
            
        Returns:
            Newly created BankAccount
            
        Raises:
            NegativeAmountError: If initial deposit is negative
        """
        logger.info(f"Creating account for: {owner}")
        
        try:
            if initial_deposit < 0:
                raise NegativeAmountError(initial_deposit, "initial deposit")
            
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
            
            logger.info(
                f"Account created: id={account_id}, owner={owner}, "
                f"initial_balance=${initial_deposit:.2f}"
            )
            return account
            
        except BankError as e:
            logger.error(f"Account creation failed: {e}")
            raise
    
    def get_account(self, account_id: str) -> BankAccount:
        """
        Get account by ID.
        
        Raises:
            AccountNotFoundError: If account doesn't exist
        """
        account = self.accounts.get(account_id)
        if account is None:
            raise AccountNotFoundError(account_id)
        return account
    
    def transfer(
        self, 
        from_id: str, 
        to_id: str, 
        amount: float,
        description: Optional[str] = None
    ) -> tuple[Transaction, Transaction]:
        """
        Transfer funds between accounts.
        
        Args:
            from_id: Source account ID
            to_id: Destination account ID
            amount: Amount to transfer
            description: Optional description
            
        Returns:
            Tuple of (withdrawal_txn, deposit_txn)
            
        Raises:
            AccountNotFoundError: If either account doesn't exist
            InsufficientFundsError: If source has insufficient funds
            NegativeAmountError: If amount is not positive
        """
        logger.info(
            f"Transfer attempt: from={from_id}, to={to_id}, amount=${amount:.2f}"
        )
        
        try:
            from_account = self.get_account(from_id)
            to_account = self.get_account(to_id)
            
            # Perform withdrawal first (may raise InsufficientFundsError)
            withdrawal = from_account.withdraw(
                amount, 
                description=f"Transfer to {to_id}" + (f": {description}" if description else "")
            )
            
            # Then deposit (should always succeed if withdrawal succeeded)
            deposit = to_account.deposit(
                amount,
                description=f"Transfer from {from_id}" + (f": {description}" if description else "")
            )
            
            logger.info(
                f"Transfer successful: from={from_id}, to={to_id}, amount=${amount:.2f}"
            )
            return withdrawal, deposit
            
        except BankError as e:
            logger.error(f"Transfer failed: {e}")
            raise


# ============================================================================
# 7. Demo with Test Cases
# ============================================================================

def demo_successful_operations() -> None:
    """Demonstrate successful banking operations."""
    print("\n" + "=" * 60)
    print("DEMO: Successful Operations")
    print("=" * 60)
    
    manager = AccountManager()
    
    # Create accounts
    alice = manager.create_account("Alice", 1000.0)
    bob = manager.create_account("Bob", 500.0)
    
    # Perform transactions
    alice.deposit(250.0, "Salary bonus")
    alice.withdraw(100.0, "Groceries")
    
    # Transfer
    manager.transfer(alice.account_id, bob.account_id, 200.0, "Rent payment")
    
    # Show statements
    print("\n" + alice.get_statement())
    print("\n" + bob.get_statement())


def demo_error_handling() -> None:
    """Demonstrate exception handling."""
    print("\n" + "=" * 60)
    print("DEMO: Error Handling")
    print("=" * 60)
    
    manager = AccountManager()
    account = manager.create_account("Charlie", 100.0)
    
    # Test 1: Insufficient funds
    print("\n[Test 1] Attempting to withdraw more than balance...")
    try:
        account.withdraw(500.0)
    except InsufficientFundsError as e:
        print(f"  ✓ Caught: {e}")
        print(f"    Shortfall: ${e.shortfall:.2f}")
    
    # Test 2: Negative amount
    print("\n[Test 2] Attempting negative deposit...")
    try:
        account.deposit(-50.0)
    except NegativeAmountError as e:
        print(f"  ✓ Caught: {e}")
    
    # Test 3: Non-existent account
    print("\n[Test 3] Attempting to get non-existent account...")
    try:
        manager.get_account("INVALID-123")
    except AccountNotFoundError as e:
        print(f"  ✓ Caught: {e}")
    
    # Test 4: Inactive account
    print("\n[Test 4] Attempting to use inactive account...")
    account.is_active = False
    try:
        account.deposit(100.0)
    except AccountInactiveError as e:
        print(f"  ✓ Caught: {e}")
    
    print("\n✓ All error cases handled correctly!")


def main() -> None:
    """Run all demos."""
    logger.info("=" * 50)
    logger.info("Bank System Demo Started")
    logger.info("=" * 50)
    
    try:
        demo_successful_operations()
        demo_error_handling()
        
        logger.info("All demos completed successfully")
        print("\n" + "=" * 60)
        print("Check 'bank.log' for detailed log output!")
        print("=" * 60)
        
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        raise
    
    finally:
        logger.info("Bank System Demo Ended")


if __name__ == "__main__":
    main()
