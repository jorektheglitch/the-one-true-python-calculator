from enum import Enum
from typing import Any, Dict, Generator, Iterable, List, Optional, Union
from typing import Generic, TypeVar

from .tokenize import TOKEN, Token, TokenizationError, tokenize


OPERATOR = Enum(
    "OPERATOR",
    "ADD UADD SUB USUB MUL DIV POW "
)
BINARY_OPS = {
    OPERATOR.ADD, OPERATOR.SUB, OPERATOR.MUL, OPERATOR.DIV, OPERATOR.POW
}
UNARY_OPS = {
    OPERATOR.UADD, OPERATOR.USUB
}
PRIORITIES = {
    OPERATOR.ADD: 1,
    OPERATOR.SUB: 1,
    OPERATOR.MUL: 2,
    OPERATOR.DIV: 2,
    OPERATOR.UADD: 3,
    OPERATOR.USUB: 3,
    OPERATOR.POW: 4
}
OPERATOR_TOKENS: Dict[TOKEN, OPERATOR] = {
    TOKEN.PLUS: OPERATOR.ADD,
    TOKEN.HYPHEN: OPERATOR.SUB,
    TOKEN.ASTERISK: OPERATOR.MUL,
    TOKEN.SLASH: OPERATOR.DIV,
    TOKEN.CARET: OPERATOR.POW
}
UNARY_OPERATOR_TOKENS: Dict[TOKEN, OPERATOR] = {
    TOKEN.PLUS: OPERATOR.UADD,
    TOKEN.HYPHEN: OPERATOR.USUB
}

Operand = Union[int, float]
StackItem = Union[OPERATOR, Operand]

T = TypeVar('T')


class ParsingError(Exception):
    """
    """


class Stack(List[T], Generic[T]):

    @property
    def top(self) -> Optional[T]:
        if self:
            return self[-1]
        return None


def build_stack(tokens: Iterable[Token]) -> Generator[StackItem, Any, None]:
    op_stack: Stack[OPERATOR] = Stack()
    last_token = None
    for token in tokens:
        if isinstance(token, str):
            value: Union[int, float]
            if "." in token:
                value = float(token)
            else:
                value = int(token)
            yield value
        elif token in OPERATOR_TOKENS:
            if token in (TOKEN.PLUS, TOKEN.HYPHEN):  # special case for + and -
                if isinstance(last_token, TOKEN) or last_token is None:
                    operator = UNARY_OPERATOR_TOKENS[token]
                else:
                    operator = OPERATOR_TOKENS[token]
            else:
                operator = OPERATOR_TOKENS[token]
            curr_priority = PRIORITIES[operator]
            top_op = op_stack.top
            ops = top_op, operator
            if not all(op is OPERATOR.POW for op in ops):
                while top_op and (curr_priority <= PRIORITIES.get(top_op, 0)):
                    yield op_stack.pop()
                    top_op = op_stack.top
            op_stack.append(operator)
        elif token is TOKEN.OPEN_PAREN:
            op_stack.append(token)  # type: ignore
        elif token is TOKEN.CLOSE_PAREN:
            while op_stack.top:
                if op_stack.top is TOKEN.OPEN_PAREN:
                    # remove open parenthesis token from op_stack
                    op_stack.pop()
                    break
                yield op_stack.pop()
            else:
                raise ParsingError("Unclosed parenthesis.")
        last_token = token
    yield from reversed(op_stack)


def parse(string: str) -> List[StackItem]:
    try:
        tokens = tokenize(string)
        stack_gen = build_stack(tokens)
        stack = list(stack_gen)
    except TokenizationError as e:
        raise ParsingError from e
    return stack
