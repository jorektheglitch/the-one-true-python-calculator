from unittest import TestCase, TestSuite, makeSuite

from calc.evaluate import evaluate


class TestNumbers(TestCase):

    def test_integer(self):
        self.assertEqual(evaluate("100"), 100)

    def test_float(self):
        self.assertEqual(evaluate("0.1"), 0.1)
        self.assertEqual(evaluate(".1"), 0.1)


class TestBasicOperations(TestCase):

    def test_addition(self):
        self.assertEqual(evaluate("1+1"), 2)

    def test_subtraction(self):
        self.assertEqual(evaluate("1-1"), 0)

    def test_multiplication(self):
        self.assertEqual(evaluate("1*1"), 1)

    def test_division(self):
        self.assertEqual(evaluate("1/2"), 0.5)

    def test_exponentiation(self):
        self.assertEqual(evaluate("2^3"), 8)

    def test_unary_addition(self):
        self.assertEqual(evaluate("+1"), 1)

    def test_unary_subtraction(self):
        self.assertEqual(evaluate("-1"), -1)

    def test_unary_subtraction_multiple(self):
        self.assertEqual(evaluate("--1"), 1)
        self.assertEqual(evaluate("---1"), -1)


class TestOperatorsPriority(TestCase):

    def test_addition_multiplication(self):
        self.assertEqual(evaluate("2+2*2"), 6)

    def test_addition_division(self):
        self.assertEqual(evaluate("2+2/2"), 3)

    def test_addition_exponentiation(self):
        self.assertEqual(evaluate("1+2^3"), 9)

    def test_subtraction_addition(self):
        self.assertEqual(evaluate("1-2+3"), 2)

    def test_subtraction_subtraction(self):
        self.assertEqual(evaluate("1-2-3"), -4)

    def test_subtraction_multiplication(self):
        self.assertEqual(evaluate("2-2*2"), -2)

    def test_subtraction_division(self):
        self.assertEqual(evaluate("2-2/2"), 1)

    def test_subtraction_exponentiation(self):
        self.assertEqual(evaluate("1-2^3"), -7)

    def test_multiplicaion_exponentiation(self):
        self.assertEqual(evaluate("2*10^2"), 200)

    def test_division_exponentiation(self):
        self.assertEqual(evaluate("1/10^2"), 0.01)

    def test_exponentiation_right_associativity(self):
        self.assertEqual(evaluate("2^3^2"), 512)

    def test_exponentiation_unary_subtraction(self):
        self.assertEqual(evaluate("2^-3"), 0.125)

    def test_unary_subtraction_exponentiation(self):
        self.assertEqual(evaluate("-2^2"), -4)


class TestEvaluation(TestCase):
    pass


evaluation_tests = TestSuite()
evaluation_tests.addTest(makeSuite(TestNumbers))
evaluation_tests.addTest(makeSuite(TestBasicOperations))
evaluation_tests.addTest(makeSuite(TestOperatorsPriority))
