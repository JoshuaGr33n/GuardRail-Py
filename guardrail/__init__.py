# """GuardRail-Py: Automated Code Compliance & Security Scanner"""
# __version__ = "0.1.0"
# __author__ = "Joshua Oleru"



"""
GuardRail-Py - Automated Code Compliance & Security Scanner

A professional static analysis toolkit for:
- AST-based code structure analysis
- Performance complexity detection (e.g. O(n²) patterns)
- Security scanning for hardcoded secrets

Built to demonstrate Lead Engineer expertise in code quality,
performance optimization, and security governance.
"""

__version__ = "0.1.0"
__author__ = "Joshua Oleru"
__license__ = "MIT"

# Export main classes from each module
from .ast_parser import ASTParser, ASTNodeInfo, NodeType, CodeLocation
from .complexity_detector import (
    ComplexityDetector,
    PerformanceWarning,
    PerformanceIssue,
)
from .secret_scanner import (
    SecretScanner,
    SecretWarning,
    SecurityIssue,
)

__all__ = [
    # AST Parser
    "ASTParser",
    "ASTNodeInfo",
    "NodeType",
    "CodeLocation",

    # Complexity Detector
    "ComplexityDetector",
    "PerformanceWarning",
    "PerformanceIssue",

    # Secret Scanner
    "SecretScanner",
    "SecretWarning",
    "SecurityIssue",
]

