"""
Complexity Detector for GuardRail-Py

Detects performance anti-patterns like O(n²) nested loops.
This demonstrates Lead Engineer skills in performance optimization and mentoring.
"""

import ast
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from guardrail.ast_parser import ASTParser, ASTNodeInfo, NodeType, CodeLocation


class PerformanceIssue(Enum):
    """Types of performance issues we can detect."""
    NESTED_LOOPS = "nested_loops"
    INEFFICIENT_DATA_STRUCTURE = "inefficient_data_structure"
    UNOPTIMIZED_STRING_CONCAT = "unoptimized_string_concat"
    UNNECESSARY_COMPUTATION = "unnecessary_computation"


@dataclass
class PerformanceWarning:
    """Represents a detected performance issue."""
    issue_type: PerformanceIssue
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    message: str
    location: CodeLocation
    filename: str
    code_snippet: str
    suggestion: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "issue_type": self.issue_type.value,
            "severity": self.severity,
            "message": self.message,
            "line": self.location.line,
            "column": self.location.column,
            "filename": self.filename,
            "code_snippet": self.code_snippet,
            "suggestion": self.suggestion
        }
    
    def __str__(self) -> str:
        return f"[{self.severity}] {self.message} at line {self.location.line}"


class ComplexityDetector:
    """
    Detects performance anti-patterns in Python code.
    
    This demonstrates Lead Engineer skills by:
    1. Identifying O(n²) algorithms that cause performance bottlenecks
    2. Providing actionable suggestions for optimization
    3. Showing experience with performance profiling and optimization
    4. Demonstrating mentoring skills through helpful suggestions
    """
    
    def __init__(self, ast_parser: ASTParser):
        """
        Initialize the complexity detector.
        
        Args:
            ast_parser: ASTParser instance with parsed code
        """
        self.parser = ast_parser
        self.warnings: List[PerformanceWarning] = []
    
    def analyze(self) -> List[PerformanceWarning]:
        """
        Analyze the code for performance issues.
        
        Returns:
            List of performance warnings found
            
        Example:
            >>> parser = ASTParser()
            >>> parser.parse_source("for i in range(10):\\n    for j in range(10): pass")
            >>> detector = ComplexityDetector(parser)
            >>> warnings = detector.analyze()
            >>> len(warnings)
            1
        """
        self.warnings = []
        
        # Run all performance checks
        self._detect_nested_loops()
        self._detect_inefficient_list_operations()
        self._detect_string_concatenation_in_loops()
        
        return self.warnings
    
    def _detect_nested_loops(self) -> None:
        """
        Detect nested loops that can cause O(n²) complexity.
        
        This is a common issue I flag when mentoring junior developers.
        Shows practical experience with performance optimization.
        """
        if not self.parser.tree:
            return
        
        class NestedLoopDetector(ast.NodeVisitor):
            """AST visitor to detect nested loops."""
            def __init__(self, detector):
                self.detector = detector
                self.current_loop = None
                self.loop_stack = []
                self.filename = detector.parser.filename or "<string>"
                self.source_lines = detector.parser._lines
            
            def visit_For(self, node):
                self._process_loop(node, "for")
            
            def visit_While(self, node):
                self._process_loop(node, "while")
            
            def visit_AsyncFor(self, node):
                self._process_loop(node, "async for")
            
            def _process_loop(self, node, loop_type):
                # Check if we're already in a loop
                if self.current_loop:
                    # We found a nested loop!
                    self._add_nested_loop_warning(node, loop_type)
                
                # Push current loop onto stack
                old_loop = self.current_loop
                self.current_loop = node
                self.loop_stack.append(node)
                
                # Visit children
                self.generic_visit(node)
                
                # Pop from stack
                self.loop_stack.pop()
                self.current_loop = self.loop_stack[-1] if self.loop_stack else None
            
            def _add_nested_loop_warning(self, node, loop_type):
                # Get the outer loop (parent in stack)
                outer_loop = self.loop_stack[-1] if self.loop_stack else None
                
                if not outer_loop:
                    return
                
                # Create warning message
                outer_type = "for" if isinstance(outer_loop, ast.For) else "while"
                if isinstance(outer_loop, ast.AsyncFor):
                    outer_type = "async for"
                
                message = (
                    f"O(n²) nested loop detected: {loop_type} loop inside {outer_type} loop. "
                    f"This can cause performance issues with large datasets."
                )
                
                # Get code snippet
                code_snippet = self._get_loop_snippet(node)
                
                # Create suggestion based on context
                suggestion = self._get_optimization_suggestion(node, outer_loop)
                
                warning = PerformanceWarning(
                    issue_type=PerformanceIssue.NESTED_LOOPS,
                    severity="HIGH",
                    message=message,
                    location=CodeLocation(
                        line=node.lineno,
                        column=node.col_offset,
                        end_line=getattr(node, 'end_lineno', None),
                        end_column=getattr(node, 'end_col_offset', None)
                    ),
                    filename=self.filename,
                    code_snippet=code_snippet,
                    suggestion=suggestion
                )
                
                self.detector.warnings.append(warning)
            
            def _get_loop_snippet(self, node):
                """Extract source code for the loop."""
                if not self.source_lines or not hasattr(node, 'lineno'):
                    return ""
                
                try:
                    start_line = max(0, node.lineno - 1 - 1)  # -1 for 0-index, -1 for context
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
            
            def _get_optimization_suggestion(self, inner_loop, outer_loop):
                """Generate helpful optimization suggestion."""
                suggestions = [
                    "Consider using vectorized operations with NumPy if working with arrays.",
                    "Look for opportunities to use list comprehensions or generator expressions.",
                    "Check if you can pre-compute values outside the inner loop.",
                    "For matrix operations, consider using specialized libraries like NumPy.",
                    "If iterating over collections, check if you need both loops or "
                    "if there's a more efficient algorithm."
                ]
                
                # Check if we're iterating over the same collection (common O(n²) pattern)
                if (isinstance(inner_loop, ast.For) and isinstance(outer_loop, ast.For)):
                    inner_iter = self._get_iterable_name(inner_loop)
                    outer_iter = self._get_iterable_name(outer_loop)
                    
                    if inner_iter and outer_iter and inner_iter == outer_iter:
                        return (
                            f"You're iterating over '{inner_iter}' twice. "
                            f"This is O(n²). Consider if you really need to compare "
                            f"each element with every other element. If you're looking "
                            f"for pairs, consider using itertools.combinations()."
                        )
                
                # Default suggestion
                return (
                    "Nested loops often indicate O(n²) complexity. "
                    "Consider: 1) Can you use a more efficient data structure? "
                    "2) Can you reduce the problem space? "
                    "3) Is there a library function that does this efficiently?"
                )
            
            def _get_iterable_name(self, for_loop):
                """Get the name of the iterable in a for loop."""
                if isinstance(for_loop.iter, ast.Name):
                    return for_loop.iter.id
                elif isinstance(for_loop.iter, ast.Call):
                    if isinstance(for_loop.iter.func, ast.Name):
                        return for_loop.iter.func.id
                return None
        
        # Run the detector
        detector = NestedLoopDetector(self)
        detector.visit(self.parser.tree)
    
    def _detect_inefficient_list_operations(self) -> None:
        """
        Detect inefficient list operations that can cause performance issues.
        
        Common issues I see when mentoring:
        - Using list.append() in loops when list comprehensions would be better
        - Repeated list concatenation
        """
        if not self.parser.tree:
            return
        
        class InefficientListVisitor(ast.NodeVisitor):
            def __init__(self, detector):
                self.detector = detector
                self.filename = detector.parser.filename or "<string>"
                self.source_lines = detector.parser._lines
                self.in_loop = False
            
            def visit_For(self, node):
                old_in_loop = self.in_loop
                self.in_loop = True
                self.generic_visit(node)
                self.in_loop = old_in_loop
            
            def visit_While(self, node):
                old_in_loop = self.in_loop
                self.in_loop = True
                self.generic_visit(node)
                self.in_loop = old_in_loop
            
            def visit_Call(self, node):
                # Check for list.append() calls inside loops
                if (self.in_loop and 
                    isinstance(node.func, ast.Attribute) and
                    node.func.attr == 'append'):
                    
                    message = (
                        "list.append() called inside loop. Consider using "
                        "list comprehension for better performance."
                    )
                    
                    code_snippet = self._get_code_snippet(node)
                    
                    warning = PerformanceWarning(
                        issue_type=PerformanceIssue.INEFFICIENT_DATA_STRUCTURE,
                        severity="MEDIUM",
                        message=message,
                        location=CodeLocation(
                            line=node.lineno,
                            column=node.col_offset
                        ),
                        filename=self.filename,
                        code_snippet=code_snippet,
                        suggestion=(
                            "Instead of using list.append() in a loop, "
                            "consider using a list comprehension: "
                            "[expression for item in iterable]. "
                            "This is often more readable and can be more efficient."
                        )
                    )
                    
                    self.detector.warnings.append(warning)
                
                self.generic_visit(node)
            
            def _get_code_snippet(self, node):
                if not self.source_lines or not hasattr(node, 'lineno'):
                    return ""
                
                try:
                    start_line = max(0, node.lineno - 1 - 1)
                    end_line = min(len(self.source_lines), node.lineno + 1)
                    return '\n'.join(self.source_lines[start_line:end_line])
                except IndexError:
                    return ""
        
        visitor = InefficientListVisitor(self)
        visitor.visit(self.parser.tree)
    
    def _detect_string_concatenation_in_loops(self) -> None:
        """
        Detect string concatenation in loops (O(n²) string operations).
        
        This is a classic performance issue that junior developers often miss.
        """
        if not self.parser.tree:
            return
        
        class StringConcatVisitor(ast.NodeVisitor):
            def __init__(self, detector):
                self.detector = detector
                self.filename = detector.parser.filename or "<string>"
                self.source_lines = detector.parser._lines
                self.in_loop = False
            
            def visit_For(self, node):
                old_in_loop = self.in_loop
                self.in_loop = True
                self.generic_visit(node)
                self.in_loop = old_in_loop
            
            def visit_While(self, node):
                old_in_loop = self.in_loop
                self.in_loop = True
                self.generic_visit(node)
                self.in_loop = old_in_loop
            
            def visit_AugAssign(self, node):
                # Check for += operator on strings in loops
                if (self.in_loop and 
                    isinstance(node.op, ast.Add) and
                    self._is_string_variable(node.target)):
                    
                    message = (
                        "String concatenation (+=) inside loop. "
                        "This creates O(n²) complexity as strings are immutable."
                    )
                    
                    code_snippet = self._get_code_snippet(node)
                    
                    warning = PerformanceWarning(
                        issue_type=PerformanceIssue.UNOPTIMIZED_STRING_CONCAT,
                        severity="MEDIUM",
                        message=message,
                        location=CodeLocation(
                            line=node.lineno,
                            column=node.col_offset
                        ),
                        filename=self.filename,
                        code_snippet=code_snippet,
                        suggestion=(
                            "Instead of using string concatenation in a loop, "
                            "consider using a list to accumulate strings and "
                            "then join them: ''.join(string_list). "
                            "This is O(n) instead of O(n²)."
                        )
                    )
                    
                    self.detector.warnings.append(warning)
                
                self.generic_visit(node)
            
            def _is_string_variable(self, node):
                """Check if a variable is likely a string."""
                # This is a simplified check - in reality, we'd need type inference
                if isinstance(node, ast.Name):
                    # Check variable name patterns that suggest strings
                    stringy_names = ['str', 'string', 'text', 'msg', 'output', 'result']
                    return any(name in node.id.lower() for name in stringy_names)
                return False
            
            def _get_code_snippet(self, node):
                if not self.source_lines or not hasattr(node, 'lineno'):
                    return ""
                
                try:
                    start_line = max(0, node.lineno - 1 - 1)
                    end_line = min(len(self.source_lines), node.lineno + 1)
                    return '\n'.join(self.source_lines[start_line:end_line])
                except IndexError:
                    return ""
        
        visitor = StringConcatVisitor(self)
        visitor.visit(self.parser.tree)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of performance issues found.
        
        Returns:
            Dictionary with summary statistics
            
        Example:
            >>> summary = detector.get_summary()
            >>> summary['total_warnings']
            2
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
            "by_severity": by_severity,
            "by_type": by_type,
            "has_nested_loops": any(
                w.issue_type == PerformanceIssue.NESTED_LOOPS 
                for w in self.warnings
            ),
            "warnings": [w.to_dict() for w in self.warnings]
        }