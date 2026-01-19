#!/usr/bin/env python3
"""
Example usage of the GuardRail-Py AST Parser.

This demonstrates how to use the AST parser feature that we've built.
"""

import sys
from guardrail.ast_parser import ASTParser


def demonstrate_ast_parser():
    """Demonstrate the capabilities of our AST parser."""
    
    # Example 1: Parse a simple function
    print("=== Example 1: Parsing Simple Function ===")
    source1 = """
def calculate_sum(numbers):
    '''Calculate the sum of a list of numbers.'''
    total = 0
    for num in numbers:
        total += num
    return total
"""
    
    parser1 = ASTParser()
    parser1.parse_source(source1, "example.py")
    
    print("✓ Code syntax is valid:", parser1.validate_syntax())
    
    functions = parser1.get_functions()
    print(f"✓ Found {len(functions)} function(s):")
    for func in functions:
        print(f"  - {func.name} at line {func.location.line}")
    
    loops = parser1.get_loops()
    print(f"✓ Found {len(loops)} loop(s)")
    
    # Example 2: Parse a file with nested loops (potential O(n²))
    print("\n=== Example 2: Detecting Nested Loops ===")
    source2 = """
def process_matrix(matrix):
    '''Process a 2D matrix - contains O(n²) nested loops.'''
    result = []
    for row in matrix:
        row_result = []
        for cell in row:  # Nested loop!
            row_result.append(cell * 2)
        result.append(row_result)
    return result
"""
    
    parser2 = ASTParser()
    parser2.parse_source(source2)
    
    analysis = parser2.analyze_complexity()
    print(f"✓ Function count: {analysis['function_count']}")
    print(f"✓ Loop count: {analysis['loop_count']}")
    print(f"✓ Has nested loops (potential O(n²)): {analysis['has_nested_loops']}")
    
    if analysis['has_nested_loops']:
        print("  ⚠️  Warning: Nested loops detected - potential performance issue!")
    
    # Example 3: Full analysis output
    print("\n=== Example 3: Full Analysis Output ===")
    source3 = """
import os
from typing import List

class DataProcessor:
    '''Process data with various methods.'''
    
    def __init__(self, config: dict):
        self.config = config
        self.api_key = "test_key"  # Hardcoded secret example
    
    def process(self, data: List[int]) -> List[int]:
        '''Process a list of integers.'''
        result = []
        for item in data:
            result.append(self._transform(item))
        return result
    
    def _transform(self, value: int) -> int:
        '''Internal transformation method.'''
        return value * self.config.get('multiplier', 1)
"""
    
    parser3 = ASTParser()
    parser3.parse_source(source3)
    
    full_analysis = parser3.to_dict()
    print("✓ Full analysis includes:")
    print(f"  - {full_analysis['node_count']} nodes analyzed")
    print(f"  - {len(full_analysis['complexity']['function_names'])} functions")
    print(f"  - {len(full_analysis['complexity']['class_names'])} classes")
    
    # Show node types found
    node_types = set(node['type'] for node in full_analysis['nodes'])
    print(f"  - Node types found: {', '.join(sorted(node_types))}")
    
    return 0


if __name__ == "__main__":
    sys.exit(demonstrate_ast_parser())