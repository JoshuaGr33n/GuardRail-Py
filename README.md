# GuardRail-Py 🔒

[![CI Status](https://github.com/yourusername/GuardRail-Py/actions/workflows/python-app.yml/badge.svg)](https://github.com/yourusername/GuardRail-Py/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Automated Code Compliance & Security Scanner for Python**
>
> Built as evidence for a **UK Global Talent Visa (Tech Nation)** application, demonstrating Lead Engineer skills in AST manipulation, security scanning, and performance optimization.

---

## 🎯 Project Vision

GuardRail-Py automates code review checks that I regularly perform as a Lead Engineer mentoring junior developers.

Rather than relying on fragile regex-based scanning, GuardRail-Py uses Python’s **Abstract Syntax Tree (AST)** to understand real code structure, enabling accurate detection of:

* 🔒 **Security vulnerabilities** (hardcoded secrets, dangerous functions)
* ⚡ **Performance issues** (O(n²) algorithms, inefficient patterns)
* 📚 **Maintainability concerns** (anti-patterns and poor practices)

---

## 🏗️ Current Status

### Phase 1: Infrastructure Setup ✅

* ✅ MIT License added
* ✅ Rules specification documented (`RULES.md`)
* ✅ CI/CD pipeline configured (GitHub Actions)
* ✅ Professional README with badges

### Phase 2: Core Features

* ✅ **Feature 1: AST Parser** (Complete)
* ✅ **Feature 2: Complexity Detector (O(n²) Checker)** (Complete)
* 🔄 Feature 3: Secret Scanner
* ⏳ Feature 4: CLI Wrapper

---

## 📦 Installation

```bash
git clone https://github.com/JoshuaGr33n/GuardRail-Py.git
cd GuardRail-Py

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

> GuardRail-Py is currently a **library-first tool**.
> A CLI wrapper will be introduced in a future phase.

---

## 🧠 Feature 1: AST Parser (Complete)

The AST Parser is the **core engine** of GuardRail-Py and demonstrates deep knowledge of Python internals.

### Example Usage

```python
from guardrail.ast_parser import ASTParser

parser = ASTParser()
parser.parse_file("example.py")

analysis = parser.analyze_complexity()
if analysis["has_nested_loops"]:
    print("⚠️ Potential O(n²) performance issue detected!")
```

A complete, runnable demonstration is available in:

```
example_usage.py
```

---

## ⚡ Feature 2: Complexity Detector (Complete)

The **Complexity Detector** identifies performance anti-patterns commonly found in real-world Python codebases, with a strong focus on **O(n²)** behavior.

### Example Usage (Manual Run)

```python
from guardrail.ast_parser import ASTParser
from guardrail.complexity_detector import ComplexityDetector

parser = ASTParser()
parser.parse_file("test_performance_issues.py")

detector = ComplexityDetector(parser)
warnings = detector.analyze()

for warning in warnings:
    print(f"{warning.severity}: {warning.message}")
```

A ready-to-run example script is provided:

```
run_detector.py
```

---

## 🌍 Real-world Validation

GuardRail-Py is validated against a deliberately inefficient Python file designed to replicate **real performance issues commonly found in junior developer submissions and legacy production code**.

The validation file:

```
test_performance_issues.py
```

Contains intentional examples of:

* O(n²) and O(n³) nested loops
* Inefficient string concatenation inside loops
* Suboptimal list-building patterns
* Repeated unnecessary computations

During validation runs, GuardRail-Py successfully detected **11 distinct performance issues**, including precise line-level locations and optimization guidance.

This demonstrates GuardRail-Py’s effectiveness at identifying **non-trivial algorithmic risks before runtime**, making it suitable for:

* Code reviews
* CI pipelines
* Performance-focused engineering workflows

---

## 🧪 Testing

All core features are covered by automated unit tests.

```bash
python -m pytest tests/
```

The test suite verifies:

* AST parsing correctness
* Complexity detection accuracy
* Edge-case handling
* Regression safety

---

## 📊 Development Timeline

* **Week 1:** Infrastructure and CI/CD setup ✅
* **Week 2:** AST Parser implementation ✅
* **Week 3:** Complexity Detector implementation ✅
* **Week 4:** Security scanning rules
* **Week 5:** CLI wrapper and packaging

---

## 👨‍💻 Author

**Joshua Oleru**
Lead Engineer applying for the **UK Global Talent Visa (Tech Nation)**

This project demonstrates:

* ✅ Advanced Python internals (AST analysis)
* ✅ Performance engineering and code review expertise
* ✅ Professional documentation and licensing
* ✅ Automated testing and CI/CD awareness
* ✅ Scalable, extensible software architecture

---

## 📄 License

This project is licensed under the **MIT License**.
See the [`LICENSE`](LICENSE) file for details.
