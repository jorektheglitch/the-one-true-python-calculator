from argparse import ArgumentParser
from typing import Optional

from .evaluate import evaluate


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
    result = evaluate(expression)
    print(result)
