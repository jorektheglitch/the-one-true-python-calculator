from enum import Enum
from string import digits

from typing import Any, Dict, Generator, Union


# сложение, вычитание, умножение, деление, числа с плавающей запятой
# возведение в степень, взятие корня n-ой степери, скобочки
TOKEN = Enum(
    "TOKEN",
    "PLUS HYPHEN ASTERISK SLASH CARET "
    # +    -      *        /     ^
    "OPEN_PAREN CLOSE_PAREN "
    # (          )
)
TOKEN_CHARS: Dict[str, TOKEN] = {
    "+": TOKEN.PLUS,
    "-": TOKEN.HYPHEN,
    "*": TOKEN.ASTERISK,
    "/": TOKEN.SLASH,
    "^": TOKEN.CARET,
    "(": TOKEN.OPEN_PAREN,
    ")": TOKEN.CLOSE_PAREN
}
Token = Union[TOKEN, str]


class TokenizationError(ValueError):

    position: int

    def __init__(self, msg, position=None) -> None:
        super().__init__(msg)
        self.position = position


def tokenize(string: str) -> Generator[Token, Any, None]:
    buffer = ""
    for i, char in enumerate(string):
        if char in digits:
            buffer += char
        elif char == ".":
            if "." in buffer:
                msg = f"Unexpected '.' symbol at position {i}."
                raise TokenizationError(msg, position=i)
            buffer += char
        elif char == " ":
            if buffer.strip():
                yield buffer
                buffer = ""
        elif char in TOKEN_CHARS:
            if buffer.strip():
                yield buffer
                buffer = ""
            token = TOKEN_CHARS[char]
            yield token
        else:
            msg = f"Unrecognizable {repr(char)} symbol at position {i}."
            raise TokenizationError(msg, position=i)
