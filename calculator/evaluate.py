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


def evaluate_stack(stack) -> Number:
    values_stack: List[Number] = []
    for item in stack:
        if isinstance(item, (int, float)):
            result = item
        elif item in BINARY_OPERATIONS:
            binop = BINARY_OPERATIONS[item]
            right = values_stack.pop()
            left = values_stack.pop()
            result = binop(left, right)
        elif item in UNARY_OPERATIONS:
            unop = UNARY_OPERATIONS[item]
            arg = values_stack.pop()
            result = unop(arg)
        values_stack.append(result)
    return values_stack[0]


def evaluate(expression: str) -> Union[int, float]:
    stack = parse(expression)
    result = evaluate_stack(stack)
    return result
