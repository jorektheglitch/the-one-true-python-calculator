from unittest import TestSuite

from .evaluation import evaluation_tests


full_suite = TestSuite()
full_suite.addTest(evaluation_tests)
