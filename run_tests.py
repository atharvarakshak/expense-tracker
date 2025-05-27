#!/usr/bin/env python3
"""
Test runner script for the expense tracker application.
"""
import unittest
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    """Run all tests in the tests directory."""
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

def run_home_route_tests():
    """Run only the home route tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName('tests.test_home_route')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'home':
        exit_code = run_home_route_tests()
    else:
        exit_code = run_tests()
    
    sys.exit(exit_code)
