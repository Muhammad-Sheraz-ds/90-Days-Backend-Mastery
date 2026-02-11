# Day 11: The Strategy Design Pattern

## 1. What is the Strategy Pattern?
The Strategy Pattern is a behavioral design pattern that lets you define a family of algorithms, put each of them into a separate class, and make their objects interchangeable.

**In simpler terms:**
It allows you to switch "strategies" (or algorithms) at runtime without changing the code that uses them.

**Why use it in Backend?**
- **Flexibility:** Swap algorithms (e.g., sorting, validation, payment processing) without modifying the core logic.
- **Testing:** You can easily mock strategies for unit tests.
- **Open/Closed Principle:** You can add new strategies without changing existing code.

---

## 2. Core Components

1.  **Strategy Interface (Abstract Base Class):** Defines the common method that all strategies must implement.
2.  **Concrete Strategies:** The actual implementations (e.g., `SortByDate`, `SortByPriority`).
3.  **Context:** The class that uses the strategy (e.g., `TaskManager`).

---

## 3. Implementation Steps

We use Python's built-in `abc` (Abstract Base Class) module to enforce the contract.

### Step 1: Define the Interface

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass
```

### Step 2: Implement Concrete Strategies

```python
class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float):
        print(f"Paying ${amount} with Credit Card.")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float):
        print(f"Paying ${amount} with PayPal.")
```

### Step 3: Use in Context

```python
class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def process_order(self, amount):
        self.strategy.pay(amount)

# Usage
processor = PaymentProcessor(CreditCardPayment())
processor.process_order(100) # Output: Paying $100 with Credit Card.

processor = PaymentProcessor(PayPalPayment())
processor.process_order(50)  # Output: Paying $50 with PayPal.
```

---

## 4. Real-World Backend Examples

1.  **Authentication:** Switching between Basic Auth, OAuth, and JWT strategies.
2.  **File Storage:** Saving files to Local Disk, AWS S3, or Google Cloud Storage. The application logic doesn't care *where* it's saved, just that it *is* saved.
3.  **Notification System:** Sending alerts via Email, SMS, or Slack based on user preference.

---

## 5. When NOT to use it?
- If you only have a few algorithms and they rarely change, a simple `if/else` block might be cleaner.
- Don't over-engineer simple problems!
