"""Run all unittest."""

import unittest

from unit_test.test_book import TestBook
from unit_test.test_user import TestUser

# Create test suite
test_suite = unittest.TestSuite()
test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUser))
test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBook))

# Run the test suite
unittest.TextTestRunner(verbosity=2).run(test_suite)
