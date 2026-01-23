"""
Secret Scanner for GuardRail-Py

Detects hardcoded secrets and sensitive credentials in Python code.
This demonstrates Lead Engineer skills in security governance and risk mitigation.
"""

import ast
import re
import string
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum

from guardrail.ast_parser import ASTParser, ASTNodeInfo, CodeLocation


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
        return f"{secret[:4]}...{secret[-4:]}" if len(secret) > 8 else "***"
    
    def __str__(self) -> str:
        return f"[{self.severity}] {self.message} at line {self.location.line}"


class SecretScanner:
    """
    Detects hardcoded secrets and sensitive credentials in Python code.
    
    This demonstrates Lead Engineer skills by:
    1. Implementing security governance and compliance checks
    2. Showing awareness of security best practices
    3. Preventing data breaches by catching secrets before commit
    4. Demonstrating knowledge of common secret patterns and formats
    """
    
    # Common secret patterns
    SECRET_PATTERNS = {
        SecurityIssue.HARDCODED_API_KEY: [
            r'sk_(live|test)_[0-9a-zA-Z]{24,}',  # Stripe secret key
            r'pk_(live|test)_[0-9a-zA-Z]{24,}',  # Stripe publishable key
            r'[0-9a-zA-Z]{40}',  # GitHub token (40 chars)
            r'eyJhbGciOiJ[0-9a-zA-Z\-_=]+\.eyJ[0-9a-zA-Z\-_=]+\.[0-9a-zA-Z\-_=]+',  # JWT pattern
        ],
        SecurityIssue.HARDCODED_PASSWORD: [
            r'password\s*=\s*["\'][^"\']{6,}["\']',
            r'passwd\s*=\s*["\'][^"\']{6,}["\']',
            r'pwd\s*=\s*["\'][^"\']{6,}["\']',
        ],
        SecurityIssue.DATABASE_URL: [
            r'(postgresql|mysql|mongodb|redis)://[^:@]+:[^@]+@',
            r'postgresql://[^:@]+:[^@]+@',
            r'mysql://[^:@]+:[^@]+@',
            r'mongodb://[^:@]+:[^@]+@',
            r'redis://[^:@]+:[^@]+@',
        ],
        SecurityIssue.AWS_KEY_PATTERN: [
            r'AKIA[0-9A-Z]{16}',
            r'aws_access_key_id\s*=\s*["\']AKIA[0-9A-Z]{16}["\']',
            r'aws_secret_access_key\s*=\s*["\'][0-9a-zA-Z/+]{40}["\']',
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
    
    # Common false positives (words that look like secrets but aren't)
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
    
    def __init__(self, ast_parser: ASTParser, strict_mode: bool = False):
        """
        Initialize the secret scanner.
        
        Args:
            ast_parser: ASTParser instance with parsed code
            strict_mode: If True, catches more potential issues (may have more false positives)
        """
        self.parser = ast_parser
        self.strict_mode = strict_mode
        self.warnings: List[SecretWarning] = []
        self.compiled_patterns = self._compile_patterns()
        self.compiled_variable_patterns = [re.compile(p, re.IGNORECASE) 
                                          for p in self.SECRET_VARIABLE_PATTERNS]
    
    def _compile_patterns(self) -> Dict[SecurityIssue, List[re.Pattern]]:
        """Compile regex patterns for efficiency."""
        compiled = {}
        for issue_type, patterns in self.SECRET_PATTERNS.items():
            compiled[issue_type] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        return compiled
    
    def analyze(self) -> List[SecretWarning]:
        """
        Analyze the code for hardcoded secrets.
        
        Returns:
            List of secret warnings found
            
        Example:
            >>> parser = ASTParser()
            >>> parser.parse_source('API_KEY = "sk_live_123456"')
            >>> scanner = SecretScanner(parser)
            >>> warnings = scanner.analyze()
            >>> len(warnings)
            1
        """
        self.warnings = []
        
        if not self.parser.tree:
            return []
        
        # Add parent references to nodes for context
        for node in ast.walk(self.parser.tree):
            for child in ast.iter_child_nodes(node):
                if not hasattr(child, 'parent'):
                    child.parent = node
        
        # Run all secret detection strategies
        self._scan_assignments_for_secrets()
        self._scan_function_calls_for_secrets()
        self._scan_string_literals_for_secrets()
        
        return self.warnings
    
    def _scan_assignments_for_secrets(self) -> None:
        """
        Scan assignment statements for potential secrets.
        
        This is the most common place where secrets get hardcoded.
        """
        class AssignmentScanner(ast.NodeVisitor):
            def __init__(self, scanner):
                self.scanner = scanner
                self.filename = scanner.parser.filename or "<string>"
                self.source_lines = scanner.parser._lines
            
            def visit_Assign(self, node):
                # Check each target in the assignment
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variable_name = target.id
                        
                        # Check if the variable name looks like it might contain a secret
                        if self._is_secret_variable_name(variable_name):
                            # Check the value being assigned
                            value = self._extract_string_value(node.value)
                            
                            if value:
                                # Check if the string value looks like a secret
                                self._check_for_secrets_in_value(
                                    node, variable_name, value, 
                                    f"Assignment to '{variable_name}'"
                                )
                
                self.generic_visit(node)
            
            def _is_secret_variable_name(self, name: str) -> bool:
                """Check if variable name suggests it might contain a secret."""
                name_lower = name.lower()
                
                # Skip common false positives
                for fp in self.scanner.FALSE_POSITIVES:
                    if fp in name_lower:
                        return False
                
                # Check against secret patterns
                for pattern in self.scanner.compiled_variable_patterns:
                    if pattern.match(name):
                        return True
                
                return False
            
            def _extract_string_value(self, node) -> Optional[str]:
                """Extract string value from AST node."""
                if isinstance(node, ast.Constant):
                    if isinstance(node.value, str):
                        return node.value
                
                elif isinstance(node, ast.JoinedStr):  # f-string
                    # Try to extract parts
                    parts = []
                    for value in node.values:
                        if isinstance(value, ast.Constant) and isinstance(value.value, str):
                            parts.append(value.value)
                        elif isinstance(value, ast.FormattedValue):
                            # Skip formatted values for simplicity
                            parts.append("{...}")
                    return ''.join(parts) if parts else None
                
                elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                    # Handle string concatenation
                    left = self._extract_string_value(node.left)
                    right = self._extract_string_value(node.right)
                    
                    if left and right:
                        return left + right
                
                elif isinstance(node, ast.Dict):
                    # Could check dict values, but skip for now
                    return None
                
                return None
            
            def _check_for_secrets_in_value(self, node, variable_name: str, 
                                          value: str, context: str):
                """Check if a string value contains a secret pattern."""
                # Skip empty or very short strings
                if not value or len(value) < 6:
                    return
                
                # Check each secret pattern
                for issue_type, patterns in self.scanner.compiled_patterns.items():
                    for pattern in patterns:
                        if pattern.search(value):
                            self._add_secret_warning(
                                node, issue_type, variable_name, value, context
                            )
                            return
                
                # Additional checks for non-pattern based secrets
                if self.scanner.strict_mode:
                    self._check_for_suspicious_string(node, variable_name, value, context)
            
            def _check_for_suspicious_string(self, node, variable_name: str, 
                                           value: str, context: str):
                """Check for suspicious strings that don't match specific patterns."""
                # Skip very short strings
                if len(value) < 10:
                    return
                
                # Check if it looks like a random string (high entropy)
                if self._looks_like_random_string(value):
                    warning = self._create_warning(
                        node=node,
                        issue_type=SecurityIssue.POTENTIAL_SECRET,
                        variable_name=variable_name,
                        secret_value=value,
                        context=context,
                        message=f"Potential secret detected in {context.lower()}",
                        severity="MEDIUM",
                        recommendation=(
                            "This looks like it might be a secret or token. "
                            "Consider using environment variables or a secrets manager."
                        ),
                        cwe_id="CWE-798"  # Use of Hard-coded Credentials
                    )
                    self.scanner.warnings.append(warning)
            
            def _looks_like_random_string(self, value: str) -> bool:
                """Heuristic check if a string looks random (potential secret)."""
                if len(value) < 20:
                    return False
                
                # Count different character types
                digit_count = sum(1 for c in value if c.isdigit())
                alpha_count = sum(1 for c in value if c.isalpha())
                special_count = len(value) - digit_count - alpha_count
                
                # Calculate ratios
                digit_ratio = digit_count / len(value)
                alpha_ratio = alpha_count / len(value)
                special_ratio = special_count / len(value)
                
                # Random strings often have mix of all types
                has_digits = digit_ratio > 0.1  # At least 10% digits
                has_letters = alpha_ratio > 0.3  # At least 30% letters
                has_special = special_ratio > 0.05  # At least 5% special chars
                
                return has_digits and has_letters and has_special
            
            def _add_secret_warning(self, node, issue_type: SecurityIssue, 
                                  variable_name: str, value: str, context: str):
                """Add a warning for a detected secret."""
                # Determine severity based on issue type
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
                
                # Create message
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
                
                # Create recommendation
                recommendation = self._get_recommendation(issue_type, variable_name)
                
                warning = self._create_warning(
                    node=node,
                    issue_type=issue_type,
                    variable_name=variable_name,
                    secret_value=value,
                    context=context,
                    message=message,
                    severity=severity,
                    recommendation=recommendation,
                    cwe_id="CWE-798"  # Use of Hard-coded Credentials
                )
                
                self.scanner.warnings.append(warning)
            
            def _get_recommendation(self, issue_type: SecurityIssue, variable_name: str) -> str:
                """Get appropriate recommendation for the issue type."""
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
                        f"Store database connection strings in environment variables or "
                        "a secrets manager. Never commit them to version control."
                    ),
                }
                
                default_rec = (
                    f"Remove the hardcoded value from '{variable_name}' and use "
                    "environment variables or a secrets management solution."
                )
                
                return recommendations.get(issue_type, default_rec)
            
            def _create_warning(self, node, issue_type: SecurityIssue, variable_name: str,
                              secret_value: str, context: str, message: str, 
                              severity: str, recommendation: str, cwe_id: str = None) -> SecretWarning:
                """Create a SecretWarning object."""
                code_snippet = self._get_code_snippet(node)
                
                return SecretWarning(
                    issue_type=issue_type,
                    severity=severity,
                    message=message,
                    location=CodeLocation(
                        line=node.lineno,
                        column=node.col_offset,
                        end_line=getattr(node, 'end_lineno', None),
                        end_column=getattr(node, 'end_col_offset', None)
                    ),
                    filename=self.filename,
                    variable_name=variable_name,
                    secret_value=secret_value,
                    code_snippet=code_snippet,
                    recommendation=recommendation,
                    cwe_id=cwe_id
                )
            
            def _get_code_snippet(self, node) -> str:
                """Extract source code snippet for a node."""
                if not self.source_lines or not hasattr(node, 'lineno'):
                    return ""
                
                try:
                    start_line = max(0, node.lineno - 1 - 1)
                    end_line = min(
                        len(self.source_lines),
                        (getattr(node, 'end_lineno', node.lineno) + 1)
                    )
                    
                    snippet_lines = []
                    for i in range(start_line, end_line):
                        snippet_lines.append(self.source_lines[i])
                    
                    return '\n'.join(snippet_lines)
                except (IndexError, AttributeError):
                    return ""
        
        # Run the scanner
        scanner = AssignmentScanner(self)
        scanner.visit(self.parser.tree)
    
    def _scan_function_calls_for_secrets(self) -> None:
        """
        Scan function calls that might be passing secrets.
        
        Example: requests.get(url, auth=('user', 'password'))
        """
        class FunctionCallScanner(ast.NodeVisitor):
            def __init__(self, scanner):
                self.scanner = scanner
                self.filename = scanner.parser.filename or "<string>"
                self.source_lines = scanner.parser._lines
            
            def visit_Call(self, node):
                # Check keyword arguments for potential secrets
                for kw in node.keywords:
                    if kw.arg:
                        arg_lower = kw.arg.lower()
                        # Check if argument name suggests it might be a secret
                        if any(secret_word in arg_lower 
                               for secret_word in ['password', 'token', 'key', 'secret', 'auth']):
                            value = self._extract_string_value(kw.value)
                            if value and len(value) > 6:
                                # Check for secret patterns
                                for issue_type, patterns in self.scanner.compiled_patterns.items():
                                    for pattern in patterns:
                                        if pattern.search(value):
                                            warning = SecretWarning(
                                                issue_type=issue_type,
                                                severity="HIGH",
                                                message=f"Potential secret passed as '{kw.arg}' argument",
                                                location=CodeLocation(
                                                    line=node.lineno,
                                                    column=node.col_offset
                                                ),
                                                filename=self.filename,
                                                variable_name=kw.arg,
                                                secret_value=value,
                                                code_snippet=self._get_code_snippet(node),
                                                recommendation=(
                                                    f"Avoid passing secrets as function arguments. "
                                                    f"Use environment variables or configuration for '{kw.arg}'."
                                                ),
                                                cwe_id="CWE-798"
                                            )
                                            self.scanner.warnings.append(warning)
                                            break
                
                # Also check positional arguments if function name suggests secrets
                if isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr.lower()
                    if any(secret_word in func_name 
                           for secret_word in ['auth', 'login', 'token', 'secret']):
                        for arg in node.args:
                            value = self._extract_string_value(arg)
                            if value and len(value) > 6:
                                self._check_argument_for_secrets(node, value, "function argument")
                
                self.generic_visit(node)
            
            def _extract_string_value(self, node):
                """Extract string value from AST node."""
                if isinstance(node, ast.Constant):
                    if isinstance(node.value, str):
                        return node.value
                    elif isinstance(node.value, (int, float, bool)):
                        return str(node.value)
                
                elif isinstance(node, ast.Tuple):
                    # Handle tuples like auth=('user', 'pass')
                    values = []
                    for elt in node.elts:
                        val = self._extract_string_value(elt)
                        if val:
                            values.append(val)
                    return tuple(values) if values else None
                
                return None
            
            def _check_argument_for_secrets(self, node, value, context: str):
                """Check if an argument value contains a secret."""
                if isinstance(value, tuple):
                    # Handle tuple values (like auth tuples)
                    for i, item in enumerate(value):
                        if isinstance(item, str) and len(item) > 6:
                            for issue_type, patterns in self.scanner.compiled_patterns.items():
                                for pattern in patterns:
                                    if pattern.search(item):
                                        warning = SecretWarning(
                                            issue_type=issue_type,
                                            severity="HIGH",
                                            message=f"Potential secret in {context}",
                                            location=CodeLocation(
                                                line=node.lineno,
                                                column=node.col_offset
                                            ),
                                            filename=self.filename,
                                            variable_name=f"arg_{i}",
                                            secret_value=item,
                                            code_snippet=self._get_code_snippet(node),
                                            recommendation="Avoid passing secrets as function arguments.",
                                            cwe_id="CWE-798"
                                        )
                                        self.scanner.warnings.append(warning)
                                        break
                elif isinstance(value, str):
                    # Check string value
                    for issue_type, patterns in self.scanner.compiled_patterns.items():
                        for pattern in patterns:
                            if pattern.search(value):
                                warning = SecretWarning(
                                    issue_type=issue_type,
                                    severity="HIGH",
                                    message=f"Potential secret in {context}",
                                    location=CodeLocation(
                                        line=node.lineno,
                                        column=node.col_offset
                                    ),
                                    filename=self.filename,
                                    variable_name=None,
                                    secret_value=value,
                                    code_snippet=self._get_code_snippet(node),
                                    recommendation="Avoid passing secrets as function arguments.",
                                    cwe_id="CWE-798"
                                )
                                self.scanner.warnings.append(warning)
                                break
            
            def _get_code_snippet(self, node):
                """Extract source code snippet."""
                if not self.source_lines or not hasattr(node, 'lineno'):
                    return ""
                
                try:
                    start_line = max(0, node.lineno - 1)
                    end_line = min(len(self.source_lines), node.lineno + 2)
                    return '\n'.join(self.source_lines[start_line:end_line])
                except IndexError:
                    return ""
        
        scanner = FunctionCallScanner(self)
        scanner.visit(self.parser.tree)
    
    def _scan_string_literals_for_secrets(self) -> None:
        """
        Scan all string literals for secret patterns.
        
        This catches secrets that aren't assigned to obvious variable names.
        """
        class StringLiteralScanner(ast.NodeVisitor):
            def __init__(self, scanner):
                self.scanner = scanner
                self.filename = scanner.parser.filename or "<string>"
                self.source_lines = scanner.parser._lines
            
            def visit_Constant(self, node):
                if isinstance(node.value, str):
                    value = node.value
                    
                    # Skip very short strings and common non-secrets
                    if len(value) < 10:
                        return
                    
                    # Skip if it's obviously not a secret
                    if any(fp in value.lower() for fp in self.scanner.FALSE_POSITIVES):
                        return
                    
                    # Skip common non-secret strings
                    if value.startswith(('http://', 'https://', '# ', '"""', "'''")):
                        return
                    
                    # Check for secret patterns
                    for issue_type, patterns in self.scanner.compiled_patterns.items():
                        for pattern in patterns:
                            if pattern.search(value):
                                self._add_string_warning(node, issue_type, value)
                                return
                
                self.generic_visit(node)
            
            def _add_string_warning(self, node, issue_type: SecurityIssue, value: str):
                """Add warning for string literal secret."""
                # Try to get context (what this string is being used for)
                context = self._get_string_context(node)
                
                warning = SecretWarning(
                    issue_type=issue_type,
                    severity="HIGH",
                    message=f"Hardcoded secret detected in {context}",
                    location=CodeLocation(
                        line=node.lineno,
                        column=node.col_offset
                    ),
                    filename=self.filename,
                    variable_name=None,
                    secret_value=value,
                    code_snippet=self._get_code_snippet(node),
                    recommendation=(
                        "Remove hardcoded secret from source code. "
                        "Use environment variables or a secrets management solution."
                    ),
                    cwe_id="CWE-798"
                )
                
                self.scanner.warnings.append(warning)
            
            def _get_string_context(self, node) -> str:
                """Determine the context of a string literal."""
                if hasattr(node, 'parent'):
                    parent = node.parent
                    
                    if parent:
                        if isinstance(parent, ast.Assign):
                            for target in parent.targets:
                                if isinstance(target, ast.Name):
                                    return f"assignment to '{target.id}'"
                                elif isinstance(target, ast.Attribute):
                                    return f"assignment to attribute"
                        elif isinstance(parent, ast.Call):
                            return "function call argument"
                        elif isinstance(parent, ast.keyword):
                            return f"keyword argument '{parent.arg}'"
                        elif isinstance(parent, ast.Dict):
                            return "dictionary value"
                
                return "string literal"
            
            def _get_code_snippet(self, node):
                """Extract source code snippet."""
                if not self.source_lines or not hasattr(node, 'lineno'):
                    return ""
                
                try:
                    start_line = max(0, node.lineno - 1)
                    end_line = min(len(self.source_lines), node.lineno + 1)
                    return '\n'.join(self.source_lines[start_line:end_line])
                except IndexError:
                    return ""
        
        scanner = StringLiteralScanner(self)
        scanner.visit(self.parser.tree)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of security issues found.
        
        Returns:
            Dictionary with summary statistics
        """
        by_severity = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }
        
        by_type = {}
        
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
            "warnings": [w.to_dict() for w in self.warnings]
        }
    
    def get_recommendations(self) -> List[str]:
        """
        Get actionable security recommendations.
        
        Returns:
            List of security improvement recommendations
        """
        recommendations = []
        
        if self.warnings:
            if any(w.severity == "CRITICAL" for w in self.warnings):
                recommendations.append(
                    "🚨 CRITICAL: Immediately rotate any exposed API keys or passwords found in this code."
                )
            
            recommendations.append(
                "🔒 Store all secrets in environment variables instead of hardcoding them."
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