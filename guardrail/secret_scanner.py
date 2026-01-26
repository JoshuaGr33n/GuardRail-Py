"""
Secret Scanner for GuardRail-Py

Detects hardcoded secrets and sensitive credentials in Python code.
This demonstrates Lead Engineer skills in security governance and risk mitigation.
"""

import ast
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from guardrail.ast_parser import ASTParser, CodeLocation


class SecurityIssue(Enum):
    """Types of security issues we can detect."""
    HARDCODED_SECRET = "hardcoded_secret"
    HARDCODED_PASSWORD = "hardcoded_password"
    HARDCODED_API_KEY = "hardcoded_api_key"
    HARDCODED_TOKEN = "hardcoded_token"
    HARDCODED_CREDENTIAL = "hardcoded_credential"
    POTENTIAL_SECRET = "potential_secret"
    AWS_KEY_PATTERN = "aws_key_pattern"
    DATABASE_URL = "database_url"


@dataclass
class SecretWarning:
    """Represents a detected secret/security issue."""
    issue_type: SecurityIssue
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    message: str
    location: CodeLocation
    filename: str
    variable_name: Optional[str]
    secret_value: Optional[str]
    code_snippet: str
    recommendation: str
    cwe_id: Optional[str] = None  # Common Weakness Enumeration ID

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "issue_type": self.issue_type.value,
            "severity": self.severity,
            "message": self.message,
            "line": self.location.line,
            "column": self.location.column,
            "filename": self.filename,
            "variable_name": self.variable_name,
            "secret_value": self._mask_secret(self.secret_value),
            "code_snippet": self.code_snippet,
            "recommendation": self.recommendation,
            "cwe_id": self.cwe_id
        }

    def _mask_secret(self, secret: Optional[str]) -> Optional[str]:
        """Mask secret value for safe display."""
        if not secret:
            return None

        if len(secret) <= 8:
            return "***"

        # Show first 4 and last 4 chars, mask the rest
        return f"{secret[:4]}...{secret[-4:]}"

    def __str__(self) -> str:
        return f"[{self.severity}] {self.message} at line {self.location.line}"


class SecretScanner:
    """
    Detects hardcoded secrets and sensitive credentials in Python code.
    """

    # Common secret patterns (value-only patterns)
    SECRET_PATTERNS = {
        SecurityIssue.HARDCODED_API_KEY: [
            r'sk_(live|test)_[0-9a-zA-Z]{24,}',  # Stripe secret key
            r'pk_(live|test)_[0-9a-zA-Z]{24,}',  # Stripe publishable key
            r'[0-9a-zA-Z]{40}',  # GitHub token (40 chars) (approx)
            r'eyJhbGciOiJ[0-9a-zA-Z\-_=]+\.eyJ[0-9a-zA-Z\-_=]+\.[0-9a-zA-Z\-_=]+',  # JWT-like
        ],
        # NOTE: We no longer rely on "password = ..." regex here because we search values.
        SecurityIssue.DATABASE_URL: [
            r'(postgresql|mysql|mongodb|redis)://[^:@]+:[^@]+@',
            r'postgresql://[^:@]+:[^@]+@',
            r'mysql://[^:@]+:[^@]+@',
            r'mongodb://[^:@]+:[^@]+@',
            r'redis://[^:@]+:[^@]+@',
        ],
        SecurityIssue.AWS_KEY_PATTERN: [
            r'AKIA[0-9A-Z]{16}',
            r'[0-9a-zA-Z/+]{40}',  # possible secret key part (used carefully w/ context)
        ]
    }

    # Variable name patterns that might indicate secrets
    SECRET_VARIABLE_PATTERNS = [
        r'.*[Aa][Pp][Ii][_.-]?[Kk]ey.*',
        r'.*[Ss]ecret.*',
        r'.*[Pp]ass(word|wd)?.*',
        r'.*[Tt]oken.*',
        r'.*[Cc]redential.*',
        r'.*[Aa]uth.*',
        r'.*[Pp]rivate.*',
        r'.*[Kk]ey.*',
    ]

    # Common false positives
    FALSE_POSITIVES = [
        "example",
        "test",
        "demo",
        "sample",
        "placeholder",
        "changeme",
        "your_",
        "dummy",
        "mock",
        "fake",
    ]

    # words for identifying password-like variable names
    _PASSWORD_NAME_HINTS = ("password", "passwd", "pwd", "passphrase")

    def __init__(self, ast_parser: ASTParser, strict_mode: bool = False):
        self.parser = ast_parser
        self.strict_mode = strict_mode
        self.warnings: List[SecretWarning] = []
        self.compiled_patterns = self._compile_patterns()
        self.compiled_variable_patterns = [re.compile(p, re.IGNORECASE)
                                           for p in self.SECRET_VARIABLE_PATTERNS]

    def _compile_patterns(self) -> Dict[SecurityIssue, List[re.Pattern]]:
        compiled: Dict[SecurityIssue, List[re.Pattern]] = {}
        for issue_type, patterns in self.SECRET_PATTERNS.items():
            compiled[issue_type] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        return compiled

    def analyze(self) -> List[SecretWarning]:
        self.warnings = []

        if not self.parser.tree:
            return []

        # Add parent references to nodes for context
        for node in ast.walk(self.parser.tree):
            for child in ast.iter_child_nodes(node):
                if not hasattr(child, "parent"):
                    child.parent = node

        self._scan_assignments_for_secrets()
        self._scan_function_calls_for_secrets()
        self._scan_string_literals_for_secrets()
        return self.warnings

    # ---------------------------
    # Assignment scanning
    # ---------------------------
    def _scan_assignments_for_secrets(self) -> None:
        class AssignmentScanner(ast.NodeVisitor):
            def __init__(self, scanner: "SecretScanner"):
                self.scanner = scanner
                self.filename = scanner.parser.filename or "<string>"
                self.source_lines = scanner.parser._lines

            def visit_Assign(self, node: ast.Assign):
                # Check each target in the assignment
                for target in node.targets:
                    if not isinstance(target, (ast.Name, ast.Attribute)):
                        continue

                    variable_name = target.id if isinstance(target, ast.Name) else target.attr
                    value = self._extract_string_value(node.value)

                    # Strict-mode heuristic should work even if variable name isn't secret-y.
                    if self.scanner.strict_mode and isinstance(value, str):
                        self._maybe_add_potential_secret(node, variable_name, value, f"Assignment to '{variable_name}'")

                    # If variable name looks secret-y, do deeper checks.
                    if self._is_secret_variable_name(variable_name) and isinstance(value, str):
                        self._check_for_secrets_in_value(node, variable_name, value, f"Assignment to '{variable_name}'")

                self.generic_visit(node)

            def _is_secret_variable_name(self, name: str) -> bool:
                name_lower = name.lower()

                for fp in self.scanner.FALSE_POSITIVES:
                    if fp in name_lower:
                        return False

                for pattern in self.scanner.compiled_variable_patterns:
                    if pattern.match(name):
                        return True
                return False

            def _extract_string_value(self, node) -> Optional[str]:
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    return node.value

                if isinstance(node, ast.JoinedStr):  # f-string
                    parts: List[str] = []
                    for v in node.values:
                        if isinstance(v, ast.Constant) and isinstance(v.value, str):
                            parts.append(v.value)
                        elif isinstance(v, ast.FormattedValue):
                            parts.append("{...}")
                    return "".join(parts) if parts else None

                if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                    left = self._extract_string_value(node.left)
                    right = self._extract_string_value(node.right)
                    if left and right:
                        return left + right

                # dict assignment handled elsewhere / by string scanning
                return None

            def _check_for_secrets_in_value(self, node, variable_name: str, value: str, context: str):
                if not value or len(value) < 6:
                    return

                # 1) Password detection based on variable name + value (fixes your test)
                if self._looks_like_password_assignment(variable_name, value):
                    self._add_secret_warning(node, SecurityIssue.HARDCODED_PASSWORD, variable_name, value, context)
                    return

                # 2) Pattern-based detection (API keys, DB URLs, AWS, JWT)
                for issue_type, patterns in self.scanner.compiled_patterns.items():
                    for pattern in patterns:
                        if pattern.search(value):
                            # Reduce accidental AWS secret key matches:
                            if issue_type == SecurityIssue.AWS_KEY_PATTERN:
                                # If it looks like AKIA..., keep it. Otherwise only treat as AWS if variable name hints AWS.
                                if not re.search(r"AKIA[0-9A-Z]{16}", value) and "aws" not in variable_name.lower():
                                    continue
                            self._add_secret_warning(node, issue_type, variable_name, value, context)
                            return

            def _looks_like_password_assignment(self, variable_name: str, value: str) -> bool:
                name_l = variable_name.lower()
                if any(h in name_l for h in self.scanner._PASSWORD_NAME_HINTS):
                    if any(fp in value.lower() for fp in self.scanner.FALSE_POSITIVES):
                        return False
                    return len(value) >= 6
                return False

            def _maybe_add_potential_secret(self, node, variable_name: str, value: str, context: str):
                # Skip obvious non-secrets
                if len(value) < 20:
                    return
                if any(fp in value.lower() for fp in self.scanner.FALSE_POSITIVES):
                    return
                if value.startswith(("http://", "https://")):
                    return

                if self._looks_like_random_string(value):
                    warning = self._create_warning(
                        node=node,
                        issue_type=SecurityIssue.POTENTIAL_SECRET,
                        variable_name=variable_name,
                        secret_value=value,
                        message=f"Potential secret detected in {context.lower()}",
                        severity="MEDIUM",
                        recommendation=(
                            "This looks like it might be a secret or token. "
                            "Consider using environment variables or a secrets manager."
                        ),
                        cwe_id="CWE-798",
                    )
                    self.scanner.warnings.append(warning)

            def _looks_like_random_string(self, value: str) -> bool:
                digit_count = sum(1 for c in value if c.isdigit())
                alpha_count = sum(1 for c in value if c.isalpha())
                special_count = len(value) - digit_count - alpha_count

                digit_ratio = digit_count / len(value)
                alpha_ratio = alpha_count / len(value)
                special_ratio = special_count / len(value)

                has_digits = digit_ratio > 0.1
                has_letters = alpha_ratio > 0.3
                has_special = special_ratio > 0.05

                return has_digits and has_letters and has_special

            def _add_secret_warning(self, node, issue_type: SecurityIssue, variable_name: str, value: str, context: str):
                severity_map = {
                    SecurityIssue.HARDCODED_API_KEY: "CRITICAL",
                    SecurityIssue.HARDCODED_PASSWORD: "CRITICAL",
                    SecurityIssue.AWS_KEY_PATTERN: "CRITICAL",
                    SecurityIssue.DATABASE_URL: "HIGH",
                    SecurityIssue.HARDCODED_TOKEN: "HIGH",
                    SecurityIssue.HARDCODED_SECRET: "HIGH",
                    SecurityIssue.HARDCODED_CREDENTIAL: "HIGH",
                }
                severity = severity_map.get(issue_type, "MEDIUM")

                message_map = {
                    SecurityIssue.HARDCODED_API_KEY: f"Hardcoded API key detected in {context.lower()}",
                    SecurityIssue.HARDCODED_PASSWORD: f"Hardcoded password detected in {context.lower()}",
                    SecurityIssue.AWS_KEY_PATTERN: f"AWS credentials detected in {context.lower()}",
                    SecurityIssue.DATABASE_URL: f"Database URL with credentials detected in {context.lower()}",
                    SecurityIssue.HARDCODED_TOKEN: f"Hardcoded token detected in {context.lower()}",
                    SecurityIssue.HARDCODED_SECRET: f"Hardcoded secret detected in {context.lower()}",
                    SecurityIssue.HARDCODED_CREDENTIAL: f"Hardcoded credentials detected in {context.lower()}",
                }
                message = message_map.get(issue_type, f"Potential security issue in {context.lower()}")

                recommendation = self._get_recommendation(issue_type, variable_name)

                warning = self._create_warning(
                    node=node,
                    issue_type=issue_type,
                    variable_name=variable_name,
                    secret_value=value,
                    message=message,
                    severity=severity,
                    recommendation=recommendation,
                    cwe_id="CWE-798",
                )
                self.scanner.warnings.append(warning)

            def _get_recommendation(self, issue_type: SecurityIssue, variable_name: str) -> str:
                recommendations = {
                    SecurityIssue.HARDCODED_API_KEY: (
                        f"Store '{variable_name}' in environment variables (os.getenv), "
                        "a secrets manager (AWS Secrets Manager, HashiCorp Vault), "
                        "or a configuration file excluded from version control."
                    ),
                    SecurityIssue.HARDCODED_PASSWORD: (
                        f"Never store passwords in source code. Use environment variables "
                        f"for '{variable_name}' or implement proper authentication flow."
                    ),
                    SecurityIssue.AWS_KEY_PATTERN: (
                        f"Use IAM roles instead of hardcoded AWS credentials for '{variable_name}'. "
                        "For development, use AWS CLI configuration or environment variables."
                    ),
                    SecurityIssue.DATABASE_URL: (
                        "Store database connection strings in environment variables or "
                        "a secrets manager. Never commit them to version control."
                    ),
                }
                default_rec = (
                    f"Remove the hardcoded value from '{variable_name}' and use "
                    "environment variables or a secrets management solution."
                )
                return recommendations.get(issue_type, default_rec)

            def _create_warning(
                self,
                node,
                issue_type: SecurityIssue,
                variable_name: str,
                secret_value: str,
                message: str,
                severity: str,
                recommendation: str,
                cwe_id: Optional[str] = None,
            ) -> SecretWarning:
                code_snippet = self._get_code_snippet(node)
                return SecretWarning(
                    issue_type=issue_type,
                    severity=severity,
                    message=message,
                    location=CodeLocation(
                        line=node.lineno,
                        column=node.col_offset,
                        end_line=getattr(node, "end_lineno", None),
                        end_column=getattr(node, "end_col_offset", None),
                    ),
                    filename=self.filename,
                    variable_name=variable_name,
                    secret_value=secret_value,
                    code_snippet=code_snippet,
                    recommendation=recommendation,
                    cwe_id=cwe_id,
                )

            def _get_code_snippet(self, node) -> str:
                if not self.source_lines or not hasattr(node, "lineno"):
                    return ""
                try:
                    start_line = max(0, node.lineno - 2)
                    end_line = min(len(self.source_lines), getattr(node, "end_lineno", node.lineno) + 1)
                    return "\n".join(self.source_lines[start_line:end_line])
                except (IndexError, AttributeError):
                    return ""

        scanner = AssignmentScanner(self)
        scanner.visit(self.parser.tree)

    # ---------------------------
    # Function-call scanning
    # ---------------------------
    def _scan_function_calls_for_secrets(self) -> None:
        class FunctionCallScanner(ast.NodeVisitor):
            def __init__(self, scanner: "SecretScanner"):
                self.scanner = scanner
                self.filename = scanner.parser.filename or "<string>"
                self.source_lines = scanner.parser._lines

            def visit_Call(self, node: ast.Call):
                for kw in node.keywords:
                    if not kw.arg:
                        continue

                    arg_lower = kw.arg.lower()
                    value = self._extract_value(kw.value)

                    # Special-case: auth=("user","pass") should flag the password
                    if kw.arg.lower() == "auth" and isinstance(value, tuple) and len(value) >= 2:
                        pwd = value[1]
                        if isinstance(pwd, str) and len(pwd) >= 6 and not self._is_false_positive(pwd):
                            self.scanner.warnings.append(
                                SecretWarning(
                                    issue_type=SecurityIssue.HARDCODED_PASSWORD,
                                    severity="CRITICAL",
                                    message="Hardcoded password detected in auth tuple",
                                    location=CodeLocation(line=node.lineno, column=node.col_offset),
                                    filename=self.filename,
                                    variable_name="auth",
                                    secret_value=pwd,
                                    code_snippet=self._get_code_snippet(node),
                                    recommendation="Use environment variables or a secrets manager for credentials.",
                                    cwe_id="CWE-798",
                                )
                            )

                    # Generic keyword secret checks (pattern-based)
                    if isinstance(value, str) and any(w in arg_lower for w in ["password", "token", "key", "secret"]):
                        if len(value) >= 6 and not self._is_false_positive(value):
                            for issue_type, patterns in self.scanner.compiled_patterns.items():
                                for pattern in patterns:
                                    if pattern.search(value):
                                        self.scanner.warnings.append(
                                            SecretWarning(
                                                issue_type=issue_type,
                                                severity="HIGH",
                                                message=f"Potential secret passed as '{kw.arg}' argument",
                                                location=CodeLocation(line=node.lineno, column=node.col_offset),
                                                filename=self.filename,
                                                variable_name=kw.arg,
                                                secret_value=value,
                                                code_snippet=self._get_code_snippet(node),
                                                recommendation=(
                                                    f"Avoid passing secrets as function arguments. "
                                                    f"Use environment variables or configuration for '{kw.arg}'."
                                                ),
                                                cwe_id="CWE-798",
                                            )
                                        )
                                        break

                self.generic_visit(node)

            def _extract_value(self, node):
                if isinstance(node, ast.Constant):
                    return node.value
                if isinstance(node, ast.Tuple):
                    out = []
                    for elt in node.elts:
                        v = self._extract_value(elt)
                        out.append(v)
                    return tuple(out)
                return None

            def _is_false_positive(self, s: str) -> bool:
                return any(fp in s.lower() for fp in self.scanner.FALSE_POSITIVES)

            def _get_code_snippet(self, node) -> str:
                if not self.source_lines or not hasattr(node, "lineno"):
                    return ""
                try:
                    start_line = max(0, node.lineno - 1)
                    end_line = min(len(self.source_lines), node.lineno + 2)
                    return "\n".join(self.source_lines[start_line:end_line])
                except IndexError:
                    return ""

        scanner = FunctionCallScanner(self)
        scanner.visit(self.parser.tree)

    # ---------------------------
    # String-literal scanning
    # ---------------------------
    def _scan_string_literals_for_secrets(self) -> None:
        class StringLiteralScanner(ast.NodeVisitor):
            def __init__(self, scanner: "SecretScanner"):
                self.scanner = scanner
                self.filename = scanner.parser.filename or "<string>"
                self.source_lines = scanner.parser._lines

            def visit_Constant(self, node: ast.Constant):
                if not isinstance(node.value, str):
                    return

                value = node.value
                if len(value) < 10:
                    return
                if any(fp in value.lower() for fp in self.scanner.FALSE_POSITIVES):
                    return
                if value.startswith(("http://", "https://", "# ", '"""', "'''")):
                    return

                for issue_type, patterns in self.scanner.compiled_patterns.items():
                    for pattern in patterns:
                        if pattern.search(value):
                            self._add_string_warning(node, issue_type, value)
                            return

                self.generic_visit(node)

            def _add_string_warning(self, node, issue_type: SecurityIssue, value: str):
                context = self._get_string_context(node)
                self.scanner.warnings.append(
                    SecretWarning(
                        issue_type=issue_type,
                        severity="HIGH",
                        message=f"Hardcoded secret detected in {context}",
                        location=CodeLocation(line=node.lineno, column=node.col_offset),
                        filename=self.filename,
                        variable_name=None,
                        secret_value=value,
                        code_snippet=self._get_code_snippet(node),
                        recommendation=(
                            "Remove hardcoded secret from source code. "
                            "Use environment variables or a secrets management solution."
                        ),
                        cwe_id="CWE-798",
                    )
                )

            def _get_string_context(self, node) -> str:
                parent = getattr(node, "parent", None)
                if parent is None:
                    return "string literal"

                if isinstance(parent, ast.Assign):
                    for target in parent.targets:
                        if isinstance(target, ast.Name):
                            return f"assignment to '{target.id}'"
                        if isinstance(target, ast.Attribute):
                            return "assignment to attribute"
                if isinstance(parent, ast.Call):
                    return "function call argument"
                if isinstance(parent, ast.keyword):
                    return f"keyword argument '{parent.arg}'"
                if isinstance(parent, ast.Dict):
                    return "dictionary value"

                return "string literal"

            def _get_code_snippet(self, node) -> str:
                if not self.source_lines or not hasattr(node, "lineno"):
                    return ""
                try:
                    start_line = max(0, node.lineno - 1)
                    end_line = min(len(self.source_lines), node.lineno + 1)
                    return "\n".join(self.source_lines[start_line:end_line])
                except IndexError:
                    return ""

        scanner = StringLiteralScanner(self)
        scanner.visit(self.parser.tree)

    # ---------------------------
    # Reporting
    # ---------------------------
    def get_summary(self) -> Dict[str, Any]:
        by_severity = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        by_type: Dict[str, int] = {}

        for warning in self.warnings:
            by_severity[warning.severity] = by_severity.get(warning.severity, 0) + 1
            issue_type = warning.issue_type.value
            by_type[issue_type] = by_type.get(issue_type, 0) + 1

        return {
            "filename": self.parser.filename or "<string>",
            "total_warnings": len(self.warnings),
            "critical_warnings": by_severity["CRITICAL"],
            "by_severity": by_severity,
            "by_type": by_type,
            "has_critical_issues": by_severity["CRITICAL"] > 0,
            "warnings": [w.to_dict() for w in self.warnings],
        }

    def get_recommendations(self) -> List[str]:
        recommendations: List[str] = []

        # Always provide at least one best-practice recommendation
        recommendations.append(
            "🔒 Store all secrets in environment variables instead of hardcoding them."
        )

        # If we found issues, add more specific guidance
        if self.warnings:
            if any(w.severity == "CRITICAL" for w in self.warnings):
                recommendations.insert(
                    0,
                    "🚨 CRITICAL: Immediately rotate any exposed API keys or passwords found in this code."
                )

            recommendations.append(
                "📦 Consider using a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.) for production."
            )
            recommendations.append(
                "🛡️ Add pre-commit hooks with GuardRail-Py to prevent committing secrets in the future."
            )

            if any(w.issue_type == SecurityIssue.DATABASE_URL for w in self.warnings):
                recommendations.append(
                    "🗄️  Use connection pooling and environment variables for database credentials."
                )

        return recommendations

