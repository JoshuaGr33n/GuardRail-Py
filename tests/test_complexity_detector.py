"""
Tests for the Complexity Detector module.

These tests demonstrate professional testing of performance analysis features.
"""

import pytest
from guardrail.ast_parser import ASTParser
from guardrail.complexity_detector import (
    ComplexityDetector, 
    PerformanceWarning,
    PerformanceIssue,
    CodeLocation
)


class TestComplexityDetector:
    """Test suite for ComplexityDetector class."""
    
    def setup_method(self):
        """Set up fresh parser and detector for each test."""
        self.parser = ASTParser()
        self.detector = None
    
    def test_detect_nested_for_loops(self):
        """Test detection of nested for loops."""
        source = """
def process_data(items):
    result = []
    for i in items:          # Outer loop
        for j in items:      # Inner loop - O(n²)!
            result.append((i, j))
    return result
"""
        
        self.parser.parse_source(source)
        self.detector = ComplexityDetector(self.parser)
        warnings = self.detector.analyze()
        
        assert len(warnings) >= 1
        assert any(w.issue_type == PerformanceIssue.NESTED_LOOPS for w in warnings)
        assert any("O(n²)" in w.message for w in warnings)
    
    def test_detect_nested_while_loops(self):
        """Test detection of nested while loops."""
        source = """
def find_pairs(numbers, target):
    i = 0
    while i < len(numbers):
        j = 0
        while j < len(numbers):  # Nested while loop
            if numbers[i] + numbers[j] == target:
                return (i, j)
            j += 1
        i += 1
    return None
"""
        
        self.parser.parse_source(source)
        self.detector = ComplexityDetector(self.parser)
        warnings = self.detector.analyze()
        
        assert len(warnings) >= 1
        assert any(w.issue_type == PerformanceIssue.NESTED_LOOPS for w in warnings)
    
    def test_detect_for_inside_while(self):
        """Test detection of for loop inside while loop."""
        source = """
def process_until_done():
    done = False
    while not done:
        for item in range(10):  # Loop inside loop
            if some_condition(item):
                done = True
                break
"""
        
        self.parser.parse_source(source)
        self.detector = ComplexityDetector(self.parser)
        warnings = self.detector.analyze()
        
        assert len(warnings) >= 1
        assert any(w.issue_type == PerformanceIssue.NESTED_LOOPS for w in warnings)
    
    def test_no_false_positive_separate_loops(self):
        """Test that separate (not nested) loops don't trigger warnings."""
        source = """
def process_items(items):
    # First loop
    for item in items:
        process(item)
    
    # Second loop (not nested)
    for item in items:
        post_process(item)
"""
        
        self.parser.parse_source(source)
        self.detector = ComplexityDetector(self.parser)
        warnings = self.detector.analyze()
        
        # Should not detect nested loops (they're sequential, not nested)
        nested_loop_warnings = [
            w for w in warnings 
            if w.issue_type == PerformanceIssue.NESTED_LOOPS
        ]
        assert len(nested_loop_warnings) == 0
    
    def test_detect_list_append_in_loop(self):
        """Test detection of list.append() inside loops."""
        source = """
def square_numbers(numbers):
    result = []
    for n in numbers:
        result.append(n * n)  # list.append() in loop
    return result
"""
        
        self.parser.parse_source(source)
        self.detector = ComplexityDetector(self.parser)
        warnings = self.detector.analyze()
        
        # Should suggest list comprehension
        assert any(
            w.issue_type == PerformanceIssue.INEFFICIENT_DATA_STRUCTURE 
            for w in warnings
        )
        assert any("list.append" in w.message for w in warnings)
    
    def test_detect_string_concatenation_in_loop(self):
        """Test detection of string concatenation in loops."""
        source = """
def build_string(items):
    result = ""
    for item in items:
        result += str(item)  # String concatenation in loop
    return result
"""
        
        self.parser.parse_source(source)
        self.detector = ComplexityDetector(self.parser)
        warnings = self.detector.analyze()
        
        assert any(
            w.issue_type == PerformanceIssue.UNOPTIMIZED_STRING_CONCAT 
            for w in warnings
        )
        assert any("String concatenation" in w.message for w in warnings)
    
    def test_triple_nested_loop(self):
        """Test detection of triple nested loops (O(n³))."""
        source = """
def process_3d(matrix):
    result = 0
    for i in matrix:
        for j in i:
            for k in j:  # Triple nested!
                result += k
    return result
"""
        
        self.parser.parse_source(source)
        self.detector = ComplexityDetector(self.parser)
        warnings = self.detector.analyze()
        
        # Should detect at least 2 nested loop warnings
        # (inner-middle and middle-outer)
        nested_warnings = [
            w for w in warnings 
            if w.issue_type == PerformanceIssue.NESTED_LOOPS
        ]
        assert len(nested_warnings) >= 2
    
    def test_get_summary(self):
        """Test summary generation."""
        source = """
def problematic_function(data):
    result = ""
    for item in data:
        for subitem in item:  # Nested
            result += subitem  # String concat
    return result
"""
        
        self.parser.parse_source(source)
        self.detector = ComplexityDetector(self.parser)
        warnings = self.detector.analyze()
        
        summary = self.detector.get_summary()
        
        assert summary['total_warnings'] == len(warnings)
        assert 'by_severity' in summary
        assert 'by_type' in summary
        assert summary['has_nested_loops'] is True
        assert 'warnings' in summary
        assert len(summary['warnings']) == len(warnings)
    
    def test_warning_structure(self):
        """Test that warnings have proper structure."""
        source = "for i in range(10):\n    for j in range(10): pass"
        
        self.parser.parse_source(source)
        self.detector = ComplexityDetector(self.parser)
        warnings = self.detector.analyze()
        
        if warnings:  # Only check if warnings were found
            warning = warnings[0]
            
            # Check required attributes
            assert hasattr(warning, 'issue_type')
            assert hasattr(warning, 'severity')
            assert hasattr(warning, 'message')
            assert hasattr(warning, 'location')
            assert hasattr(warning, 'filename')
            assert hasattr(warning, 'code_snippet')
            assert hasattr(warning, 'suggestion')
            
            # Check location
            assert hasattr(warning.location, 'line')
            assert hasattr(warning.location, 'column')
            
            # Check to_dict method
            warning_dict = warning.to_dict()
            assert 'line' in warning_dict
            assert 'message' in warning_dict
            assert 'suggestion' in warning_dict
    
    def test_empty_code(self):
        """Test analysis of empty code."""
        source = ""
        
        self.parser.parse_source(source)
        self.detector = ComplexityDetector(self.parser)
        warnings = self.detector.analyze()
        
        assert len(warnings) == 0
    
    def test_complex_real_world_example(self):
        """Test a more complex real-world example."""
        source = """
def find_duplicate_pairs(strings):
    '''Find all duplicate pairs in a list of strings.'''
    duplicates = []
    
    # O(n²) algorithm - common beginner mistake
    for i in range(len(strings)):
        for j in range(len(strings)):
            if i != j and strings[i] == strings[j]:
                duplicates.append((i, j))
    
    # Build result string inefficiently
    result = ""
    for pair in duplicates:
        result += f"Pair: {pair}\\n"
    
    return result
"""
        
        self.parser.parse_source(source)
        self.detector = ComplexityDetector(self.parser)
        warnings = self.detector.analyze()
        
        # Should find multiple issues
        assert len(warnings) >= 2
        
        # Check for specific issues
        has_nested_loops = any(
            w.issue_type == PerformanceIssue.NESTED_LOOPS 
            for w in warnings
        )
        has_string_concat = any(
            w.issue_type == PerformanceIssue.UNOPTIMIZED_STRING_CONCAT 
            for w in warnings
        )
        
        assert has_nested_loops
        assert has_string_concat


def test_performance_warning_dataclass():
    """Test PerformanceWarning dataclass."""
    location = CodeLocation(line=10, column=5)
    warning = PerformanceWarning(
        issue_type=PerformanceIssue.NESTED_LOOPS,
        severity="HIGH",
        message="Test warning",
        location=location,
        filename="test.py",
        code_snippet="for i in items:",
        suggestion="Use a better algorithm"
    )
    
    assert warning.issue_type == PerformanceIssue.NESTED_LOOPS
    assert warning.severity == "HIGH"
    assert warning.message == "Test warning"
    assert warning.location == location
    assert warning.filename == "test.py"
    
    # Test to_dict
    warning_dict = warning.to_dict()
    assert warning_dict['issue_type'] == 'nested_loops'
    assert warning_dict['severity'] == 'HIGH'
    assert warning_dict['line'] == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])