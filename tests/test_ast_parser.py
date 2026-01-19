"""
Tests for the AST Parser module.

These tests demonstrate professional testing practices expected from a Lead Engineer.
"""

import pytest
import tempfile
import os
from guardrail.ast_parser import ASTParser, NodeType, ASTNodeInfo, CodeLocation


class TestASTParser:
    """Test suite for ASTParser class."""
    
    def setup_method(self):
        """Set up fresh parser for each test."""
        self.parser = ASTParser()
    
    def test_parse_valid_source_code(self):
        """Test parsing valid Python source code."""
        source = """
def hello(name: str) -> str:
    '''Greet someone.'''
    return f"Hello, {name}!"

class Greeter:
    '''A simple greeter class.'''
    
    def __init__(self, prefix: str = "Hello"):
        self.prefix = prefix
    
    def greet(self, name: str) -> str:
        return f"{self.prefix}, {name}!"
"""
        
        tree = self.parser.parse_source(source)
        assert tree is not None
        assert self.parser.validate_syntax() is True
    
    def test_parse_file(self):
        """Test parsing a Python file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
def example():
    for i in range(10):
        print(i)
""")
            temp_file = f.name
        
        try:
            tree = self.parser.parse_file(temp_file)
            assert tree is not None
            assert self.parser.filename == temp_file
        finally:
            os.unlink(temp_file)
    
    def test_syntax_error_handling(self):
        """Test graceful handling of syntax errors."""
        invalid_source = "def invalid syntax:"
        
        with pytest.raises(SyntaxError) as exc_info:
            self.parser.parse_source(invalid_source)
        
        assert "Syntax error" in str(exc_info.value)
    
    def test_file_not_found(self):
        """Test error when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            self.parser.parse_file("/nonexistent/file.py")
    
    def test_get_functions(self):
        """Test extracting function information."""
        source = """
def func1():
    pass

def func2(x: int) -> int:
    return x * 2
"""
        
        self.parser.parse_source(source)
        functions = self.parser.get_functions()
        
        assert len(functions) == 2
        assert functions[0].name == "func1"
        assert functions[0].node_type == NodeType.FUNCTION
        assert functions[1].name == "func2"
    
    def test_get_classes(self):
        """Test extracting class information."""
        source = """
class BaseClass:
    pass

class DerivedClass(BaseClass):
    def method(self):
        pass
"""
        
        self.parser.parse_source(source)
        classes = self.parser.get_classes()
        
        assert len(classes) == 2
        assert classes[0].name == "BaseClass"
        assert classes[1].name == "DerivedClass"
        assert classes[1].attributes['bases'] == 1
    
    def test_get_loops(self):
        """Test extracting loop information."""
        source = """
for i in range(10):
    print(i)

while True:
    break
"""
        
        self.parser.parse_source(source)
        loops = self.parser.get_loops()
        
        assert len(loops) == 2
        assert loops[0].name == "for_loop"
        assert loops[1].name == "while_loop"
    
    def test_get_assignments(self):
        """Test extracting assignment information."""
        source = """
x = 10
y, z = 20, 30
self.value = "test"
"""
        
        self.parser.parse_source(source)
        assignments = self.parser.get_assignments()
        
        assert len(assignments) >= 2  # Might find more depending on implementation
        # The first assignment should have 'x' in its targets
        assert any('x' in assignment.attributes.get('targets', []) 
                  for assignment in assignments)
    
    def test_analyze_complexity(self):
        """Test complexity analysis."""
        source = """
def process_data(items):
    result = []
    for item in items:
        for subitem in item:
            result.append(subitem * 2)
    return result
"""
        
        self.parser.parse_source(source)
        analysis = self.parser.analyze_complexity()
        
        assert analysis['function_count'] == 1
        assert analysis['loop_count'] == 2
        assert analysis['has_nested_loops'] is True
        assert 'process_data' in analysis['function_names']
    
    def test_has_nested_loops_detection(self):
        """Test detection of nested loops."""
        # Test with nested loops
        source_with_nested = """
for i in range(10):
    for j in range(10):
        print(i, j)
"""
        self.parser.parse_source(source_with_nested)
        assert self.parser._has_nested_loops() is True
        
        # Test without nested loops
        source_simple = """
for i in range(10):
    print(i)
for j in range(10):
    print(j)
"""
        self.parser = ASTParser()  # Fresh parser
        self.parser.parse_source(source_simple)
        assert self.parser._has_nested_loops() is False
    
    def test_get_source_snippet(self):
        """Test extracting source code snippets."""
        source = """
def example():
    # This is a function
    x = 10
    return x
"""
        
        self.parser.parse_source(source)
        functions = self.parser.get_functions()
        
        assert len(functions) == 1
        snippet = self.parser.get_source_snippet(functions[0], context_lines=1)
        assert "def example():" in snippet
        assert "return x" in snippet
    
    def test_to_dict_serialization(self):
        """Test converting analysis to dictionary."""
        source = "def test(): pass"
        self.parser.parse_source(source)
        
        result = self.parser.to_dict()
        
        assert 'filename' in result
        assert 'node_count' in result
        assert 'syntax_valid' in result
        assert 'nodes' in result
        assert 'complexity' in result
        assert result['syntax_valid'] is True
    
    def test_empty_source(self):
        """Test parsing empty source code."""
        tree = self.parser.parse_source("")
        assert tree is not None
        # Empty module is valid Python
    
    def test_unicode_source(self):
        """Test parsing source with unicode characters."""
        source = """
def greet(name: str) -> str:
    return f"Hello, {name}! 👋"
"""
        
        tree = self.parser.parse_source(source)
        assert tree is not None
        assert self.parser.validate_syntax() is True
    
    def test_decorated_function(self):
        """Test parsing functions with decorators."""
        source = """
@decorator1
@decorator2
def decorated():
    pass
"""
        
        self.parser.parse_source(source)
        functions = self.parser.get_functions()
        
        assert len(functions) == 1
        assert functions[0].attributes['decorators'] == 2


def test_code_location_dataclass():
    """Test CodeLocation dataclass."""
    location = CodeLocation(line=10, column=5)
    assert location.line == 10
    assert location.column == 5
    assert location.end_line is None
    assert location.end_column is None


def test_ast_node_info_dataclass():
    """Test ASTNodeInfo dataclass."""
    location = CodeLocation(line=1, column=0)
    info = ASTNodeInfo(
        node_type=NodeType.FUNCTION,
        name="test_function",
        location=location,
        parent=None,
        attributes={"args": 2}
    )
    
    assert info.node_type == NodeType.FUNCTION
    assert info.name == "test_function"
    assert info.location == location
    assert info.attributes["args"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])