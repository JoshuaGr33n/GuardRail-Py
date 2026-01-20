from guardrail.ast_parser import ASTParser
from guardrail.complexity_detector import ComplexityDetector

parser = ASTParser()
parser.parse_file("test_performance_issues.py")

detector = ComplexityDetector(parser)
warnings = detector.analyze()

print(f"Found {len(warnings)} performance issues in test_performance_issues.py")
for w in warnings[:5]:
    print(f"  • {w.message} (line {w.location.line})")
