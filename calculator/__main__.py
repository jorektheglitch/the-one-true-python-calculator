from argparse import ArgumentParser
from typing import Optional

from .evaluate import evaluate, EvaluationError


parser = ArgumentParser(description='Calculator')
parser.add_argument('expression', nargs='?')

args = parser.parse_args()
expression: Optional[str] = args.expression

if expression is None:  # expression does not specified
    parser.print_help()
elif not expression:  # expression is empty string
    print("Please specify expression string.")
else:
    expression = expression.strip("\"\'")
    try:
        result = evaluate(expression)
    except EvaluationError as e:
        print(f"{type(e).__name__}: {e}")
        exit_code = 1
    else:
        print(result)
        exit_code = 0
    exit(exit_code)
