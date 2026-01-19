# GuardRail-Py Rules Specification

## Overview

**GuardRail-Py** is an automated code compliance checker that scans Python code for **security**, **performance**, and **maintainability** issues using **Abstract Syntax Tree (AST)** analysis.

---

## Rule Categories

## 🔒 Security Rules

### Rule SEC-001: Hardcoded Secrets

* **Description:** Detects sensitive credentials stored in plain text.
* **Patterns:** Variable names containing:

  * `API_KEY`
  * `SECRET`
  * `PASSWORD`
  * `TOKEN`
  * `CREDENTIAL`
* **Severity:** **CRITICAL**

**Example:**

```python
# ❌ Will be flagged
API_KEY = "sk_live_1234567890"
database_password = "SuperSecret123"
```

---

### Rule SEC-002: Dangerous Functions

* **Description:** Flags usage of potentially dangerous functions.
* **Patterns:**

  * `eval()` with user input
  * `exec()` with user input
  * `pickle.loads()` from untrusted sources
* **Severity:** **HIGH**

**Example:**

```python
# ❌ Will be flagged
result = eval(user_input)
```

---

## ⚡ Performance Rules

### Rule PERF-001: O(n²) Nested Loops

* **Description:** Detects nested loops that can cause quadratic time complexity.
* **Patterns:**

  * `for` loops inside `for` loops
  * `while` loops inside `for` loops
* **Severity:** **HIGH**

**Example:**

```python
# ❌ Will be flagged
for i in items:
    for j in items:  # Nested loop
        process(i, j)
```

---

## 📚 Documentation Rules

### Rule DOC-001: Missing Docstrings

* **Description:** Ensures public functions and classes have documentation.
* **Patterns:**

  * Functions without docstrings
  * Classes without docstrings
* **Severity:** **MEDIUM**

**Example:**

```python
# ❌ Will be flagged
def process_data(data):  # No docstring
    return data * 2
```

---

## 🎨 Code Quality Rules

### Rule QUAL-001: PEP 8 Violations

* **Description:** Enforces Python style guide compliance.
* **Patterns:**

  * Lines longer than 79 characters
  * Missing trailing newline
  * Multiple statements per line
* **Severity:** **LOW**

---

## Implementation Notes

All rules are implemented using **Python’s `ast` module** for accurate structural analysis rather than regex-based text matching.
