from unittest import TestSuite, makeSuite

from .test_evaluation import evaluation_tests
from .test_parsing import TestParsing
from .test_tokenization import TestTokenization


full_suite = TestSuite()
full_suite.addTest(evaluation_tests)
