# GuardRail-Py 🔒

[![CI Status](https://github.com/yourusername/GuardRail-Py/actions/workflows/python-app.yml/badge.svg)](https://github.com/yourusername/GuardRail-Py/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Automated Code Compliance & Security Scanner for Python**
>
> Built as evidence for a **UK Global Talent Visa (Tech Nation)** application, demonstrating Lead Engineer skills in AST manipulation, security scanning, and performance optimization.

---

## 🎯 Project Vision

GuardRail-Py automates code review checks that I frequently perform as a Lead Engineer mentoring junior developers.
Instead of relying on regex-based text scanning, it uses Python’s **Abstract Syntax Tree (AST)** to understand code structure, enabling accurate detection of:

* 🔒 **Security vulnerabilities** (hardcoded secrets, dangerous functions)
* ⚡ **Performance issues** (O(n²) algorithms, inefficient patterns)
* 📚 **Maintainability concerns** (missing documentation, style violations)

---

## 🏗️ Current Status

### Phase 1: Infrastructure Setup ✅

* ✅ MIT License added
* ✅ Rules specification documented (`RULES.md`)
* ✅ CI/CD pipeline configured (GitHub Actions)
* ✅ Professional README with badges

### Phase 2: Core Features

* ✅ **Feature 1: AST Parser** (Complete)
* 🔄 Feature 2: Complexity Detector (O(n²) checker)
* ⏳ Feature 3: Secret Scanner
* ⏳ Feature 4: CLI Wrapper

---

## 🧠 Feature 1: AST Parser (Complete)

The AST Parser is the **core engine** of GuardRail-Py and demonstrates deep knowledge of Python internals.

### Key Capabilities

1. **Structural Code Analysis** using Python’s `ast` module
2. **Visitor Pattern Architecture** for extensibility
3. **Complexity Analysis** (nested loops, function depth)
4. **Graceful Error Handling** for syntax issues
5. **Comprehensive Test Coverage**

### Example Usage

```python
from guardrail.ast_parser import ASTParser

parser = ASTParser()

# Parse a Python file
parser.parse_file("example.py")

# Inspect code structure
functions = parser.get_functions()
classes = parser.get_classes()
loops = parser.get_loops()

# Detect potential performance issues
analysis = parser.analyze_complexity()
if analysis["has_nested_loops"]:
    print("⚠️ Potential O(n²) performance issue detected!")
```

### Lead Engineer Skills Demonstrated

* ✅ Deep Python Internals (AST module)
* ✅ Software Architecture (Visitor pattern)
* ✅ Testing & Quality (pytest-based test suite)
* ✅ Robust Error Handling
* ✅ Clear Documentation

---

## 📋 Rules Implemented

See [`RULES.md`](RULES.md) for a full specification of all security, performance, and quality rules enforced by GuardRail-Py.

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/GuardRail-Py.git
cd GuardRail-Py

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies (once packaging is added)
pip install -e .

# Run the AST parser example
python example_usage.py
```

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run tests with coverage
python -m pytest tests/ --cov=guardrail --cov-report=html

# Run a specific test
python -m pytest tests/test_ast_parser.py -v
```

---

## 📊 Development Timeline

* **Week 1:** Infrastructure setup ✅
* **Week 2:** AST Parser implementation ✅
* **Week 3:** Complexity & security checkers (in progress)
* **Week 4:** CLI wrapper and packaging
* **Week 5:** Final testing and documentation

---

## 👨‍💻 Author

**Joshua Oleru**
Lead Engineer applying for **UK Global Talent Visa (Tech Nation)**

This project demonstrates:

* ✅ DevOps & CI/CD (GitHub Actions)
* ✅ Professional documentation standards
* ✅ Automated testing (pytest)
* ✅ Code quality enforcement
* ✅ Advanced Python internals
* ✅ Scalable software architecture

---

## 📄 License

This project is licensed under the **MIT License**.
See the [`LICENSE`](LICENSE) file for details.
