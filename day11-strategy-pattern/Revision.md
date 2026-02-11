# Revision: Day 10 & 11 (Backend Mastery)

## Day 10: Magic Methods (Dunder Methods)

**What:** Special methods starting/ending with `__` (e.g., `__init__`, `__str__`) that let objects behave like built-in types.

| Method | Purpose | Backend Use Case |
| :--- | :--- | :--- |
| `__str__` | User-friendly string. | Logging, UI display (Django Admin). |
| `__repr__` | Unambiguous dev string. | Debugging in console/logs. **Always implement this.** |
| `__eq__` | Equality check (`==`). | comparing DB entities (e.g., `user1 == user2`). |
| `__lt__` | Sorting (`<`). | `sorted(tasks)` by priority or date. |
| `__len__` | Object length (`len()`). | Counting items in a custom collection/queryset. |
| `__getitem__` | Indexing/Iteration. | Making objects iterable (`for x in obj`). |

**Key Takeaway:** Magic methods make your code *expressive* and *clean*. Instead of `manager.get_task(0)`, you can just use `manager[0]`.

---

## Day 11: Strategy Design Pattern

**What:** A behavioral pattern that lets you swap algorithms at runtime. Define a family of algorithms, encapsulate each one, and make them interchangeable.

**Structure:**
1.  **Strategy Interface (ABC):** The contract (e.g., `PaymentStrategy` with `pay()` method).
2.  **Concrete Strategy:** The implementation (e.g., `CreditCardPayment`, `PayPalPayment`).
3.  **Context:** The class using the strategy (e.g., `PaymentProcessor`).

**Why we use it:**
- **Open/Closed Principle:** Add new strategies (e.g., `BitcoinPayment`) without changing existing code.
- **Runtime Flexibility:** Switch sorting/filtering logic based on user input.
- **Testability:** Mock complex logic easily.

**Backend Example:**
- **FastAPI Dependency Injection:** Swapping a real database service with a mock one for testing.
- **Authentication:** Choosing between `BasicAuth`, `BearerToken`, or `APIKey` based on config.
