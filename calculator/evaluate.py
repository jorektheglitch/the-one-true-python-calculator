from operator import add, mul, sub, truediv
from typing import Callable, Dict, List, Union
from .parse import OPERATOR, parse


Number = Union[int, float]
BinaryOp = Callable[[Number, Number], Number]
UnaryOp = Callable[[Number], Number]

BINARY_OPERATIONS: Dict[OPERATOR, BinaryOp] = {
    OPERATOR.ADD: add,
    OPERATOR.SUB: sub,
    OPERATOR.MUL: mul,
    OPERATOR.DIV: truediv,
    OPERATOR.POW: pow,
}
UNARY_OPERATIONS: Dict[OPERATOR, UnaryOp] = {
    OPERATOR.UADD: lambda n: n,
    OPERATOR.USUB: lambda n: -n
}


class EvaluationError(Exception):
    pass


def evaluate_stack(stack) -> Number:
    values_stack: List[Number] = []
    for item in stack:
        if isinstance(item, (int, float)):
            result = item
        elif item in BINARY_OPERATIONS:
            binop = BINARY_OPERATIONS[item]
            try:
                right = values_stack.pop()
                left = values_stack.pop()
            except IndexError:
                raise EvaluationError
            result = binop(left, right)
        elif item in UNARY_OPERATIONS:
            unop = UNARY_OPERATIONS[item]
            try:
                arg = values_stack.pop()
            except IndexError:
                raise EvaluationError
            result = unop(arg)
        values_stack.append(result)
    result, *remaining = values_stack
    if remaining:
        msg = "Multiple values on stack at the end of evaluation."
        raise EvaluationError(msg)
    return result


def evaluate(expression: str) -> Union[int, float]:
    stack = parse(expression)
    result = evaluate_stack(stack)
    return result
