# GuardRail-Py 🔒

[![CI Status](https://github.com/yourusername/GuardRail-Py/actions/workflows/python-app.yml/badge.svg)](https://github.com/yourusername/GuardRail-Py/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Automated Code Compliance & Security Scanner for Python**
>
> Built as evidence for a **UK Global Talent Visa (Tech Nation)** application, demonstrating Lead Engineer skills in **AST manipulation, security scanning, performance analysis, and scalable tooling design**.

---

## 🎯 Project Vision

GuardRail-Py automates code review checks that I regularly perform as a **Lead Engineer mentoring junior developers**.

Instead of relying on fragile regex-based scanning, GuardRail-Py uses Python’s **Abstract Syntax Tree (AST)** to understand real code structure, enabling accurate detection of:

- 🔒 **Security vulnerabilities** (hardcoded secrets, credentials, API keys)
- ⚡ **Performance issues** (O(n²) and higher complexity patterns)
- 📚 **Maintainability concerns** (anti-patterns and poor practices)

The goal is to catch **real-world engineering risks before runtime**, during code review or CI.

---

## 🏗️ Current Status

### **Phase 1: Infrastructure Setup** ✅
- ✅ MIT License added
- ✅ Rules specification documented (`RULES.md`)
- ✅ CI/CD pipeline configured (GitHub Actions)
- ✅ Professional README with badges

### **Phase 2: Core Features**
- ✅ **Feature 1: AST Parser** (Complete!)
- ✅ **Feature 2: Complexity Detector (O(n²) Checker)** (Complete!)
- ✅ **Feature 3: Secret Scanner (Security)** (Complete!)
- 🔄 Feature 4: CLI Wrapper

---

## 📦 Installation

```bash
git clone https://github.com/JoshuaGr33n/GuardRail-Py.git
cd GuardRail-Py

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
````

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

A complete runnable example is available in:

```
example_usage.py
```

---

## ⚡ Feature 2: Complexity Detector (Complete)

The **Complexity Detector** identifies performance anti-patterns commonly found in real-world Python codebases, with a strong focus on **O(n²)** and higher-order complexity.

### Example Usage

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

## 🔒 Feature 3: Secret Scanner (Complete!)

The **Secret Scanner** detects **hardcoded secrets, API keys, passwords, and sensitive credentials** in Python source code.

This feature demonstrates **security governance and compliance awareness** expected of a Lead Engineer.

### 🔑 Key Capabilities

1. **API Key Detection**

   * Stripe, GitHub tokens, JWTs, etc.
2. **Password Detection**

   * Hardcoded passwords in variables
3. **AWS Credential Detection**

   * Access keys and secret keys
4. **Database URL Detection**

   * Connection strings with embedded credentials
5. **Heuristic Analysis**

   * Identifies potential secrets via entropy and naming patterns
6. **CWE Compliance**

   * Maps findings to **CWE-798 (Use of Hard-coded Credentials)**
7. **Actionable Recommendations**

   * Clear remediation guidance for each finding

---

### 🛠️ Technical Implementation

```python
from guardrail.ast_parser import ASTParser
from guardrail.secret_scanner import SecretScanner

parser = ASTParser()
parser.parse_file("code_with_secrets.py")

scanner = SecretScanner(parser)
warnings = scanner.analyze()

for warning in warnings:
    print(f"🔒 {warning.severity}: {warning.message}")
    print(f"   Variable: {warning.variable_name}")
    print(f"   Recommendation: {warning.recommendation}")
    print(f"   CWE: {warning.cwe_id}")
```

---

### 📄 Example Output

```text
[GUARDRAIL-PY] Security Analysis Report
=======================================
File: config.py
Total warnings: 3 (2 CRITICAL, 1 HIGH)

[CRITICAL] Hardcoded API key detected in assignment to 'STRIPE_SECRET_KEY'
           Location: line 15
           Value: sk_live_49J4...F8EJ
           CWE: CWE-798
           Recommendation: Store 'STRIPE_SECRET_KEY' in environment variables...

[CRITICAL] Hardcoded password detected in assignment to 'DATABASE_PASSWORD'
           Location: line 22
           Value: P@ssw0rd123!
           Recommendation: Never store passwords in source code...

[HIGH] Database URL with credentials detected in assignment to 'DATABASE_URL'
        Location: line 30
        Value: postgresql://admin:***@localhost/mydb
        Recommendation: Store database connection strings in environment variables...
```

---

### 🧠 Security Patterns Detected

* Stripe API keys (`sk_live_`, `sk_test_`)
* AWS credentials (`AKIA...`, secret keys)
* JWT tokens
* Database URLs with embedded credentials
* Generic secrets in variables like `PASSWORD`, `SECRET`, `KEY`
* High-entropy strings likely representing secrets

---

### 👨‍💼 Lead Engineer Skills Demonstrated

* ✅ **Security Governance** – Preventing credential leaks and breaches
* ✅ **Compliance Knowledge** – CWE-798 and secure coding standards
* ✅ **Risk Mitigation** – Proactive vulnerability detection
* ✅ **Best Practices** – Secrets management awareness
* ✅ **Professional Reporting** – Clear, actionable security feedback

---

## 🔍 Analyzing Your Own Code

GuardRail-Py can analyze **any Python file or codebase**.

### Single File

```python
parser = ASTParser()
parser.parse_file("path/to/your_code.py")

detector = ComplexityDetector(parser)
warnings = detector.analyze()
```

### Multiple Files

```python
files = [
    "src/module_a.py",
    "src/module_b.py",
    "scripts/data_processing.py",
]

parser = ASTParser()
for file_path in files:
    parser.parse_file(file_path)

detector = ComplexityDetector(parser)
warnings = detector.analyze()

print(f"Found {len(warnings)} potential issues")
```

Suitable for:

* Code reviews
* CI/CD pipelines
* Pre-commit hooks
* Static analysis workflows

---

## 🌍 Real-world Validation

GuardRail-Py is validated against deliberately inefficient and insecure Python files designed to replicate **real issues found in production and junior submissions**.

Validation includes detection of:

* O(n²) and O(n³) nested loops
* Inefficient string concatenation
* Suboptimal list-building
* Hardcoded secrets and credentials

During validation runs, GuardRail-Py detected **multiple performance and security issues with line-level accuracy**, proving its effectiveness in **preventing real engineering risks before deployment**.

---

## 🧪 Testing

All core features are covered by automated unit tests.

```bash
python -m pytest tests/
```

Test coverage includes:

* AST parsing correctness
* Complexity detection accuracy
* Secret scanning reliability
* Edge-case handling
* Regression safety

---

## 📊 Development Timeline

* **Week 1:** Infrastructure and CI/CD setup ✅
* **Week 2:** AST Parser implementation ✅
* **Week 3:** Complexity Detector implementation ✅
* **Week 4:** Secret Scanner & security rules ✅
* **Week 5:** CLI wrapper and packaging 🔄

---

## 👨‍💻 Author

**Joshua Oleru**
Lead Engineer applying for the **UK Global Talent Visa (Tech Nation)**

This project demonstrates:

* Advanced Python internals (AST analysis)
* Performance engineering expertise
* Security governance and compliance awareness
* Professional documentation and CI/CD
* Scalable, extensible software architecture

---

## 📄 License

This project is licensed under the **MIT License**.
See the [`LICENSE`](LICENSE) file for details.




