#!/bin/bash

# Create a 'tests' folder
mkdir -p tests

# Move test files into the 'tests' folder
mv test_cli.py tests/
mv test_data_access_layer.py tests/

touch __init__.py
touch tests/__init__.py


# Create the test runner Python script
cat > tests/test_runner.py << EOL
import unittest
import sys

class TestRunner:
    def __init__(self):
        self.loader = unittest.TestLoader()
        self.runner = unittest.TextTestRunner()

    def run_tests(self, test_cases=None):
        if test_cases:
            suite = self.loader.loadTestsFromName(','.join(test_cases))
        else:
            suite = self.loader.discover('tests')

        self.runner.run(suite)

if __name__ == "__main__":
    print("Select the test cases to run (or press Enter to run all):")
    print("1. test_cli.py")
    print("2. test_data_access_layer.py")

    test_cases = []

    while True:
        user_input = input("Enter test case number or 'r' to run tests: ").strip()
        if user_input.lower() == "r":
            break
        elif user_input == "1":
            test_cases.append("tests.test_cli")
        elif user_input == "2":
            test_cases.append("tests.test_data_access_layer")
        else:
            print("Invalid input. Please enter a valid test case number or 'r'.")

    runner = TestRunner()
    runner.run_tests(test_cases)
EOL

echo "Project structure reorganized, and test runner script created."
