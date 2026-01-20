#!/usr/bin/env python3
"""
Verify that all GuardRail-Py features work correctly.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and print results."""
    print(f"\n🔧 {description}")
    print(f"   Command: {command}")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Success")
            if result.stdout.strip():
                print(f"Output:\n{result.stdout[:500]}")  # First 500 chars
        else:
            print("❌ Failed")
            print(f"Return code: {result.returncode}")
            if result.stderr:
                print(f"Error:\n{result.stderr}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Timeout after 30 seconds")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    """Run all verification steps."""
    print("=" * 70)
    print("GUARDRAIL-PY: COMPLETE VERIFICATION SCRIPT")
    print("=" * 70)
    
    successes = 0
    total = 0
    
    # 1. Check Python version
    total += 1
    if run_command("python --version", "Check Python version"):
        successes += 1
    
    # 2. Run example usage
    total += 1
    if run_command("python example_usage.py", "Run example usage demonstration"):
        successes += 1
    
    # 3. Run AST parser tests
    total += 1
    if run_command("python -m pytest tests/test_ast_parser.py -v", "Run AST parser tests"):
        successes += 1
    
    # 4. Run complexity detector tests
    total += 1
    if run_command("python -m pytest tests/test_complexity_detector.py -v", "Run complexity detector tests"):
        successes += 1
    
    # 5. Run all tests
    total += 1
    if run_command("python -m pytest tests/ -v", "Run all tests"):
        successes += 1
    
    # 6. Test with coverage
    total += 1
    if run_command("python -m pytest tests/ --cov=guardrail --cov-report=term", "Run tests with coverage"):
        successes += 1
    
    # 7. Test the performance issues file
    total += 1
    if run_command("python test_performance_issues.py", "Test performance issues file"):
        successes += 1
    
    # 8. Lint check
    total += 1
    if run_command("python -m py_compile guardrail/*.py", "Check Python syntax"):
        successes += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"✅ Successes: {successes}/{total}")
    print(f"📊 Score: {(successes/total)*100:.1f}%")
    
    if successes == total:
        print("\n🎉 ALL TESTS PASSED! GuardRail-Py is ready for commit.")
        return 0
    else:
        print(f"\n⚠️  {total-successes} test(s) failed. Please check above output.")
        return 1

if __name__ == "__main__":
    sys.exit(main())