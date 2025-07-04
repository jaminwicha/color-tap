#!/usr/bin/env python3
"""
Test runner script for Color Tap game
Runs all unit tests with coverage reporting
"""

import subprocess
import sys
import os

def run_tests():
    """Run all tests with coverage reporting"""
    print("🧪 Running Color Tap test suite...")
    print("=" * 50)
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    try:
        # Run pytest with coverage
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "--verbose",
            "--tb=short", 
            "--cov=.",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--ignore=_archive",
            "--ignore=level_data",
            "tests/"
        ], check=True)
        
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/index.html")
        return True
        
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 50)
        print("❌ Tests failed!")
        print(f"Exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)