import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from test_cli import TestCLI
from test_data_access_layer import TestDatabaseMethods
import traceback

class ProgressIndicator(unittest.TestResult):
    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        print(f"Running test: {test}")

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        print("PASSED")

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        print("FAILED")

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        print("ERROR")
        traceback.print_exception(*err)

class TestRunner:
    def __init__(self):
        self.runner = unittest.TextTestRunner(resultclass=ProgressIndicator, verbosity=2)

    def run_tests(self, test_cases):
        suite = unittest.TestSuite()
        for test_case in test_cases:
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_case))
        self.runner.run(suite)

if __name__ == "__main__":
    runner = TestRunner()

    test_cases = [
        TestCLI,
        TestDatabaseMethods
    ]

    user_input = input("Select the test cases to run (or press Enter to run all):\n"
                       "1. test_cli.py\n"
                       "2. test_data_access_layer.py\n"
                       "Enter test case number or 'r' to run tests: ")

    if user_input == '1':
        test_cases = [TestCLI]
    elif user_input == '2':
        test_cases = [TestDatabaseMethods]
    elif user_input != 'r':
        print("Invalid input. Running all tests.")

    runner.run_tests(test_cases)
