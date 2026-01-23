#!/usr/bin/env python3
"""
GuardRail-Py: Complete Example Usage with Features 1–3
Demonstrates:
1. AST Parser
2. Complexity Detector
3. Secret Scanner

This script showcases professional, real-world capabilities built for
the UK Global Talent Visa (Tech Nation).
"""

import sys
import os
from pathlib import Path

# Ensure local package resolution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from guardrail.ast_parser import ASTParser
from guardrail.complexity_detector import ComplexityDetector, PerformanceIssue
from guardrail.secret_scanner import SecretScanner, SecurityIssue


def print_header(title: str):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


# ============================================================================
# FEATURE 1: AST PARSER
# ============================================================================

def demo_feature_1_ast_parser():
    print_header("FEATURE 1: AST PARSER (The Brain)")

    print("""
The AST Parser demonstrates deep understanding of Python internals by
analyzing real code structure using the Abstract Syntax Tree.
""")

    source = '''
def example_function(data):
    """Example function for demonstration."""
    result = []
    for item in data:
        result.append(item * 2)
    return result
'''

    parser = ASTParser()
    parser.parse_source(source, "demo.py")

    print("✅ Code parsed and validated successfully")
    print(f"✅ Functions found: {len(parser.get_functions())}")
    print(f"✅ Loops found: {len(parser.get_loops())}")

    return parser


# ============================================================================
# FEATURE 2: COMPLEXITY DETECTOR
# ============================================================================

def demo_feature_2_complexity_detector():
    print_header("FEATURE 2: COMPLEXITY DETECTOR (O(n²) Checker)")

    print("""
Detects performance anti-patterns that commonly appear in junior
developer submissions and legacy production systems.
""")

    source = '''
def process_matrix(matrix):
    result = []
    for row in matrix:
        for cell in row:  # O(n²)
            result.append(cell * 2)
    return result

def build_string_inefficient(items):
    output = ""
    for item in items:
        output += str(item)  # String concatenation in loop
    return output
'''

    parser = ASTParser()
    parser.parse_source(source, "performance_issues.py")

    detector = ComplexityDetector(parser)
    warnings = detector.analyze()

    print(f"✅ Found {len(warnings)} performance warnings")

    for warning in warnings:
        print(f"  • {warning.severity}: {warning.message} (line {warning.location.line})")

    return detector


# ============================================================================
# FEATURE 3: SECRET SCANNER
# ============================================================================

def demo_feature_3_secret_scanner():
    print_header("FEATURE 3: SECRET SCANNER (Security)")

    print("""
Detects hardcoded credentials and secrets that pose serious security risks.
Demonstrates security governance and risk mitigation skills.
""")

    source = '''
# ❌ INTENTIONAL SECURITY ISSUES

STRIPE_SECRET_KEY = "sk_live_49J4D9F849JF84JF8EJF84EJF8EJ"
DATABASE_PASSWORD = "SuperSecret123!"
DATABASE_URL = "postgresql://admin:password@localhost/mydb"

# ✅ Secure approach
# import os
# API_KEY = os.getenv("STRIPE_API_KEY")
'''

    parser = ASTParser()
    parser.parse_source(source, "security_issues.py")

    scanner = SecretScanner(parser)
    warnings = scanner.analyze()

    print(f"✅ Found {len(warnings)} security warnings")

    for warning in warnings[:3]:
        print(f"\n  🔒 {warning.severity}")
        print(f"     {warning.message}")
        print(f"     Variable: {warning.variable_name}")
        print(f"     Line: {warning.location.line}")
        print(f"     Recommendation: {warning.recommendation}")

    return scanner


# ============================================================================
# COMPLETE WORKFLOW DEMO
# ============================================================================

def demonstrate_complete_workflow():
    print_header("COMPLETE REAL-WORLD WORKFLOW")

    print("""
Analyzing a realistic Python file containing BOTH performance
and security issues — exactly how GuardRail-Py would be used in practice.
""")

    test_code = '''
STRIPE_API_KEY = "sk_live_123456789"
DB_PASSWORD = "password123"

def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                duplicates.append(items[i])
    return duplicates
'''

    test_file = Path("demo_real_world.py")
    test_file.write_text(test_code)

    try:
        parser = ASTParser()
        parser.parse_file(str(test_file))

        perf_detector = ComplexityDetector(parser)
        perf_warnings = perf_detector.analyze()

        sec_scanner = SecretScanner(parser)
        sec_warnings = sec_scanner.analyze()

        print(f"⚠️  Performance issues: {len(perf_warnings)}")
        print(f"🔒 Security issues: {len(sec_warnings)}")

    finally:
        test_file.unlink()
        print("🧹 Cleaned up demo file")


# ============================================================================
# LEAD ENGINEER VALUE
# ============================================================================

def demonstrate_lead_engineer_value():
    print_header("LEAD ENGINEER VALUE DEMONSTRATED")

    print("""
This project demonstrates:

• Performance mentoring via static analysis (Feature 2)
• Security governance and compliance (Feature 3)
• Deep Python internals knowledge (Feature 1)
• CI/CD-ready tooling for real teams
• Automation of code review best practices
""")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("GUARDRAIL-PY: AUTOMATED CODE COMPLIANCE SCANNER")

    demo_feature_1_ast_parser()
    demo_feature_2_complexity_detector()
    demo_feature_3_secret_scanner()
    demonstrate_complete_workflow()
    demonstrate_lead_engineer_value()

    print("\n🎉 DEMONSTRATION COMPLETE")
    print("Next: Feature 4 — CLI Wrapper")


if __name__ == "__main__":
    main()
