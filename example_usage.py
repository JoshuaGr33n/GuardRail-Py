# #!/usr/bin/env python3
# """
# Example usage of the GuardRail-Py AST Parser.

# This demonstrates how to use the AST parser feature that we've built.
# """

# import sys
# from guardrail.ast_parser import ASTParser


# def demonstrate_ast_parser():
#     """Demonstrate the capabilities of our AST parser."""
    
#     # Example 1: Parse a simple function
#     print("=== Example 1: Parsing Simple Function ===")
#     source1 = """
# def calculate_sum(numbers):
#     '''Calculate the sum of a list of numbers.'''
#     total = 0
#     for num in numbers:
#         total += num
#     return total
# """
    
#     parser1 = ASTParser()
#     parser1.parse_source(source1, "example.py")
    
#     print("✓ Code syntax is valid:", parser1.validate_syntax())
    
#     functions = parser1.get_functions()
#     print(f"✓ Found {len(functions)} function(s):")
#     for func in functions:
#         print(f"  - {func.name} at line {func.location.line}")
    
#     loops = parser1.get_loops()
#     print(f"✓ Found {len(loops)} loop(s)")
    
#     # Example 2: Parse a file with nested loops (potential O(n²))
#     print("\n=== Example 2: Detecting Nested Loops ===")
#     source2 = """
# def process_matrix(matrix):
#     '''Process a 2D matrix - contains O(n²) nested loops.'''
#     result = []
#     for row in matrix:
#         row_result = []
#         for cell in row:  # Nested loop!
#             row_result.append(cell * 2)
#         result.append(row_result)
#     return result
# """
    
#     parser2 = ASTParser()
#     parser2.parse_source(source2)
    
#     analysis = parser2.analyze_complexity()
#     print(f"✓ Function count: {analysis['function_count']}")
#     print(f"✓ Loop count: {analysis['loop_count']}")
#     print(f"✓ Has nested loops (potential O(n²)): {analysis['has_nested_loops']}")
    
#     if analysis['has_nested_loops']:
#         print("  ⚠️  Warning: Nested loops detected - potential performance issue!")
    
#     # Example 3: Full analysis output
#     print("\n=== Example 3: Full Analysis Output ===")
#     source3 = """
# import os
# from typing import List

# class DataProcessor:
#     '''Process data with various methods.'''
    
#     def __init__(self, config: dict):
#         self.config = config
#         self.api_key = "test_key"  # Hardcoded secret example
    
#     def process(self, data: List[int]) -> List[int]:
#         '''Process a list of integers.'''
#         result = []
#         for item in data:
#             result.append(self._transform(item))
#         return result
    
#     def _transform(self, value: int) -> int:
#         '''Internal transformation method.'''
#         return value * self.config.get('multiplier', 1)
# """
    
#     parser3 = ASTParser()
#     parser3.parse_source(source3)
    
#     full_analysis = parser3.to_dict()
#     print("✓ Full analysis includes:")
#     print(f"  - {full_analysis['node_count']} nodes analyzed")
#     print(f"  - {len(full_analysis['complexity']['function_names'])} functions")
#     print(f"  - {len(full_analysis['complexity']['class_names'])} classes")
    
#     # Show node types found
#     node_types = set(node['type'] for node in full_analysis['nodes'])
#     print(f"  - Node types found: {', '.join(sorted(node_types))}")
    
#     return 0


# if __name__ == "__main__":
#     sys.exit(demonstrate_ast_parser())




#!/usr/bin/env python3
"""
GuardRail-Py: Complete Example Usage
Demonstrates both AST Parser (Feature 1) and Complexity Detector (Feature 2)

This script showcases the professional capabilities built for the UK Global Talent Visa.
"""

import sys
import os
from pathlib import Path

# Add the guardrail module to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from guardrail.ast_parser import ASTParser, NodeType
from guardrail.complexity_detector import ComplexityDetector, PerformanceIssue


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def demo_feature_1_ast_parser():
    """Demonstrate Feature 1: AST Parser capabilities."""
    print_header("FEATURE 1: AST PARSER (The 'Brain')")
    
    print("""
The AST Parser demonstrates deep understanding of Python internals by using
the Abstract Syntax Tree module instead of regex-based text scanning.
""")
    
    # Example 1: Basic parsing
    print("\n📋 Example 1: Basic Code Structure Analysis")
    print("-" * 50)
    
    source = '''
def calculate_stats(data: list) -> dict:
    """Calculate basic statistics for a dataset."""
    total = sum(data)
    count = len(data)
    
    # Calculate mean
    mean = total / count if count > 0 else 0
    
    # Calculate variance
    variance = 0
    for value in data:
        variance += (value - mean) ** 2
    variance = variance / count if count > 0 else 0
    
    return {
        "count": count,
        "mean": mean,
        "variance": variance
    }

class DataProcessor:
    """Process and analyze data."""
    
    def __init__(self, config: dict):
        self.config = config
        self.results = []
    
    def process(self, dataset):
        """Process the dataset."""
        for item in dataset:
            transformed = self._transform(item)
            self.results.append(transformed)
        return self.results
    
    def _transform(self, value):
        """Internal transformation method."""
        return value * self.config.get("multiplier", 1)
'''
    
    parser = ASTParser()
    parser.parse_source(source, "statistics.py")
    
    print("✅ Code parsed successfully")
    print(f"✅ Syntax validation: {parser.validate_syntax()}")
    
    # Get analysis
    nodes = parser.get_node_info()
    analysis = parser.analyze_complexity()
    
    print(f"\n📊 Code Analysis Results:")
    print(f"   • Total nodes analyzed: {len(nodes)}")
    print(f"   • Functions found: {analysis['function_count']}")
    print(f"   • Classes found: {analysis['class_count']}")
    print(f"   • Loops found: {analysis['loop_count']}")
    print(f"   • Max nesting depth: {analysis['max_nesting_depth']}")
    print(f"   • Has nested loops: {analysis['has_nested_loops']}")
    
    # Show function details
    print(f"\n🔍 Function Details:")
    functions = parser.get_functions()
    for func in functions:
        print(f"   • {func.name}() at line {func.location.line}")
        if func.attributes.get('args', 0) > 0:
            print(f"     Takes {func.attributes['args']} arguments")
    
    # Example 2: Error handling
    print("\n\n📋 Example 2: Professional Error Handling")
    print("-" * 50)
    
    invalid_source = "def broken_function( :  # Missing closing paren"
    
    try:
        parser2 = ASTParser()
        parser2.parse_source(invalid_source, "broken.py")
        print("❌ This should not print - code has syntax error")
    except SyntaxError as e:
        print("✅ Correctly caught syntax error:")
        print(f"   Error: {str(e).split(':')[-1].strip()}")
    
    # Example 3: File parsing
    print("\n\n📋 Example 3: File System Integration")
    print("-" * 50)
    
    # Create a temporary test file
    test_file = Path("test_example.py")
    test_file.write_text('''
def test_function():
    """Test function for demonstration."""
    x = [i * 2 for i in range(10)]
    return x
''')
    
    try:
        parser3 = ASTParser()
        parser3.parse_file(str(test_file))
        print(f"✅ Successfully parsed file: {test_file}")
        print(f"✅ File contains {len(parser3.get_functions())} function(s)")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()
    
    return parser


def demo_feature_2_complexity_detector(parser=None):
    """Demonstrate Feature 2: Complexity Detector capabilities."""
    print_header("FEATURE 2: COMPLEXITY DETECTOR (O(n²) Checker)")
    
    print("""
The Complexity Detector demonstrates performance optimization expertise by
identifying common anti-patterns that cause O(n²) complexity issues.
As a Lead Engineer, I frequently mentor junior developers on these issues.
""")
    
    # Example 1: Classic O(n²) nested loop
    print("\n📋 Example 1: Detecting Nested Loops (Classic O(n²))")
    print("-" * 50)
    
    source1 = '''
def find_all_pairs(items):
    """Find all possible pairs (naive O(n²) approach)."""
    pairs = []
    
    # COMMON JUNIOR DEVELOPER MISTAKE
    for i in range(len(items)):
        for j in range(len(items)):  # NESTED LOOP - O(n²)!
            if i != j:
                pairs.append((items[i], items[j]))
    
    return pairs

def build_combinations_inefficient(list1, list2):
    """Build all combinations inefficiently."""
    combinations = []
    
    # ANOTHER NESTED LOOP PATTERN
    for item1 in list1:
        for item2 in list2:  # O(n*m) complexity
            combinations.append(f"{item1}-{item2}")
    
    return combinations
'''
    
    parser1 = parser or ASTParser()
    parser1.parse_source(source1, "nested_loops.py")
    
    detector1 = ComplexityDetector(parser1)
    warnings1 = detector1.analyze()
    
    print(f"✅ Analyzed code with {len(warnings1)} performance warnings")
    
    # Filter for nested loop warnings
    nested_warnings = [w for w in warnings1 if w.issue_type == PerformanceIssue.NESTED_LOOPS]
    
    if nested_warnings:
        print(f"\n⚠️  Found {len(nested_warnings)} nested loop issue(s):")
        for i, warning in enumerate(nested_warnings, 1):
            print(f"\n   {i}. {warning.severity} severity at line {warning.location.line}")
            print(f"      Message: {warning.message}")
            print(f"      Suggestion: {warning.suggestion}")
    else:
        print("✅ No nested loops detected (unexpected for this example)")
    
    # Example 2: String concatenation in loops
    print("\n\n📋 Example 2: String Concatenation Anti-Pattern")
    print("-" * 50)
    
    source2 = '''
def generate_report(users):
    """Generate a report with inefficient string building."""
    report = "USER REPORT\\n"
    report += "=" * 20 + "\\n"
    
    # COMMON PERFORMANCE PITFALL
    for user in users:
        report += f"User: {user['name']}\\n"
        report += f"  Email: {user['email']}\\n"
        
        for order in user['orders']:  # Nested loop too!
            report += f"    Order: {order['id']} - ${order['amount']}\\n"
    
    return report

def build_csv(data_rows):
    """Build CSV string inefficiently."""
    csv = "id,name,value\\n"
    
    for row in data_rows:
        # String concatenation in loop - O(n²) for strings!
        csv += f"{row['id']},{row['name']},{row['value']}\\n"
    
    return csv
'''
    
    parser2 = ASTParser()
    parser2.parse_source(source2, "string_issues.py")
    
    detector2 = ComplexityDetector(parser2)
    warnings2 = detector2.analyze()
    
    print(f"✅ Found {len(warnings2)} performance issues")
    
    # Group warnings by type
    string_warnings = [w for w in warnings2 if w.issue_type == PerformanceIssue.UNOPTIMIZED_STRING_CONCAT]
    list_warnings = [w for w in warnings2 if w.issue_type == PerformanceIssue.INEFFICIENT_DATA_STRUCTURE]
    
    if string_warnings:
        print(f"\n⚠️  String concatenation issues: {len(string_warnings)}")
        print(f"   Example suggestion: {string_warnings[0].suggestion}")
    
    if list_warnings:
        print(f"\n⚠️  List operation issues: {len(list_warnings)}")
    
    # Example 3: Professional summary report
    print("\n\n📋 Example 3: Professional Summary Report")
    print("-" * 50)
    
    summary = detector2.get_summary()
    
    print(f"📄 Analysis Report for: {summary['filename']}")
    print(f"📊 Total warnings: {summary['total_warnings']}")
    
    print("\n📈 Severity Breakdown:")
    for severity, count in sorted(summary['by_severity'].items(), 
                                  key=lambda x: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].index(x[0])):
        if count > 0:
            print(f"   • {severity}: {count}")
    
    print("\n🔧 Issue Type Breakdown:")
    for issue_type, count in summary['by_type'].items():
        print(f"   • {issue_type.replace('_', ' ').title()}: {count}")
    
    print(f"\n🎯 Has nested loops: {summary['has_nested_loops']}")
    
    # Example 4: Optimized code comparison
    print("\n\n📋 Example 4: Optimized Code (No Warnings)")
    print("-" * 50)
    
    source3 = '''
def find_all_pairs_optimized(items):
    """Optimized approach using itertools."""
    from itertools import combinations
    return list(combinations(items, 2))

def generate_report_optimized(users):
    """Generate report efficiently with list join."""
    report_lines = ["USER REPORT", "=" * 20]
    
    for user in users:
        report_lines.append(f"User: {user['name']}")
        report_lines.append(f"  Email: {user['email']}")
        
        order_lines = []
        for order in user['orders']:
            order_lines.append(f"    Order: {order['id']} - ${order['amount']}")
        
        if order_lines:
            report_lines.extend(order_lines)
    
    return "\\n".join(report_lines)

def build_csv_optimized(data_rows):
    """Build CSV efficiently."""
    header = "id,name,value"
    rows = [f"{row['id']},{row['name']},{row['value']}" for row in data_rows]
    return header + "\\n" + "\\n".join(rows)
'''
    
    parser3 = ASTParser()
    parser3.parse_source(source3, "optimized.py")
    
    detector3 = ComplexityDetector(parser3)
    warnings3 = detector3.analyze()
    
    if len(warnings3) == 0:
        print("✅ No performance issues detected in optimized code!")
        print("✅ This demonstrates proper implementation of best practices")
    else:
        print(f"⚠️  Unexpected: Found {len(warnings3)} issues in 'optimized' code")
        for warning in warnings3:
            print(f"   - {warning.message}")
    
    return detector2


def demonstrate_lead_engineer_insights():
    """Show how this demonstrates Lead Engineer skills for the visa."""
    print_header("LEAD ENGINEER SKILLS DEMONSTRATED")
    
    print("""
For my UK Global Talent Visa (Tech Nation) application, this project shows:

1. TECHNICAL LEADERSHIP
   • Mentoring junior developers on performance optimization
   • Establishing code quality standards and best practices
   • Automating code review processes to scale team effectiveness

2. INNOVATION
   • Using AST-based analysis instead of simple regex matching
   • Context-aware suggestions that vary based on code patterns
   • Professional reporting that integrates into development workflows

3. IMPACT
   • Preventing production performance issues before deployment
   • Educational tool that teaches developers about algorithmic complexity
   • Scalable solution that saves hundreds of hours in code reviews

4. PROFESSIONAL DEVELOPMENT PRACTICES
   • Complete CI/CD pipeline with GitHub Actions
   • Comprehensive test suite with edge cases
   • Professional documentation and examples
   • Modular, extensible architecture using design patterns
""")
    
    print("\n" + "=" * 70)
    print(" REAL-WORLD APPLICATION")
    print("=" * 70)
    
    print("""
As a Lead Engineer at [Your Company], I've:
• Mentored 5+ junior developers on performance optimization
• Reduced API response times by 60% by fixing O(n²) algorithms
• Implemented code review automation that saves 10+ hours per week
• Established performance benchmarks and monitoring for critical services

This tool encapsulates that experience and makes it available to other teams.
""")


def run_self_check():
    """Run GuardRail-Py on its own source code."""
    print_header("SELF-CHECK: Running GuardRail-Py on Itself")
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    
    # Check the ast_parser.py file
    ast_parser_file = script_dir / "guardrail" / "ast_parser.py"
    
    if ast_parser_file.exists():
        print(f"🔍 Analyzing: {ast_parser_file}")
        
        parser = ASTParser()
        try:
            parser.parse_file(str(ast_parser_file))
            detector = ComplexityDetector(parser)
            warnings = detector.analyze()
            
            if warnings:
                print(f"⚠️  Found {len(warnings)} potential issues in our own code:")
                for warning in warnings[:3]:  # Show first 3
                    print(f"   • {warning.message} (line {warning.location.line})")
                print("   (Showing first 3 issues)")
            else:
                print("✅ No performance issues detected in our AST parser!")
                
        except Exception as e:
            print(f"❌ Error during self-check: {e}")
    else:
        print("⚠️  Could not find ast_parser.py for self-check")
    
    return True


def main():
    """Main demonstration function."""
    print("\n" + "=" * 70)
    print(" GUARDRAIL-PY: Automated Code Compliance Checker")
    print(" Built for UK Global Talent Visa (Tech Nation) Application")
    print("=" * 70)
    
    print("""
This tool demonstrates Lead Engineer skills in:
• Python AST module for deep code analysis
• Performance optimization and mentoring
• Security scanning and best practices
• Professional software development lifecycle
""")
    
    try:
        # Run all demonstrations
        parser = demo_feature_1_ast_parser()
        detector = demo_feature_2_complexity_detector(parser)
        
        # Optional: Run self-check
        if "--self-check" in sys.argv:
            run_self_check()
        
        demonstrate_lead_engineer_insights()
        
        print("\n" + "=" * 70)
        print(" ✅ DEMONSTRATION COMPLETE")
        print("=" * 70)
        
        print("\n🎯 Next steps for the Global Talent Visa application:")
        print("1. Push Feature 2 with detailed commit message")
        print("2. Take screenshots of commit history showing progression")
        print("3. Document how this shows Technical Leadership")
        print("4. Prepare explanation for Tech Nation assessor")
        print("5. Continue with Feature 3: Secret Scanner")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    # Check for command line arguments
    if "--help" in sys.argv or "-h" in sys.argv:
        print("""
GuardRail-Py Example Usage
        
Usage:
  python example_usage.py          # Run full demonstration
  python example_usage.py --self-check   # Also run GuardRail-Py on itself
        
This demonstrates the capabilities built for the UK Global Talent Visa.
""")
        sys.exit(0)
    
    exit_code = main()
    sys.exit(exit_code)