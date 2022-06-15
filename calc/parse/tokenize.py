from enum import Enum
from string import digits

from typing import Any, Dict, Generator, Optional, Union


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
    yield_buffer: bool = False
    token: Optional[TOKEN] = None
    last_token: Optional[Token] = None
    for i, char in enumerate(string):
        if char in digits:
            buffer += char
        elif char == ".":
            if "." in buffer:
                msg = f"Unexpected '.' symbol at position {i}."
                raise TokenizationError(msg, position=i)
            buffer += char
        elif char == " ":
            yield_buffer = True
        elif char in TOKEN_CHARS:
            yield_buffer = True
            token = TOKEN_CHARS[char]
        else:
            msg = f"Unrecognizable {repr(char)} symbol at position {i}."
            raise TokenizationError(msg, position=i)
        if yield_buffer:
            buffer = buffer.strip()
            if buffer:
                if isinstance(last_token, str):
                    # handling for two digits ("1 1") situation
                    msg = f"Missing operation between {last_token} and {token}."  # noqa
                    raise TokenizationError(msg)
                last_token = buffer
                yield buffer
            buffer = ""
            yield_buffer = False
        if token is not None:
            current_pair = (last_token, token)
            if all(isinstance(t, TOKEN) for t in current_pair):
                if token not in (TOKEN.HYPHEN, TOKEN.PLUS):
                    # handling for two operators ("- *") situation
                    msg = f"Unexpected {repr(char)} operator."
                    raise TokenizationError(msg)
            last_token = token
            yield token
            token = None
    buffer = buffer.strip()
    if buffer:
        yield buffer
