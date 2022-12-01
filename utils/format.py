import json
import random
import re
from typing import Optional, Union


def formatCookie(cookie_string: Optional[str] = None) -> Optional[Union[str, dict]]:
    if cookie_string is None:
        return None

    cookies = {}
    cookie_items = cookie_string.split("; ")
    for item in cookie_items:
        key, value = item.split("=")
        cookies[key] = value

    return cookies


def formatPayload(payload: bytes) -> Union[str, dict]:
    payload_string = payload.decode("utf-8")

    try:
        return json.loads(payload_string)
    except json.JSONDecodeError:
        return payload_string


def is_escaped(position: int, string: str):
    usable = string[:position][::-1]
    match = re.search(r"^\\*", usable)
    if match:
        match = match.group()
        if len(match) == 1:
            return True
        elif len(match) % 2 == 0:
            return False
        else:
            return True
    else:
        return False


def strip(string, substring, direction="right"):
    done = False
    strippedString = ""
    if direction == "right":
        string = string[::-1]
    for char in string:
        if char == substring and not done:
            done = True
        else:
            strippedString += char
    if direction == "right":
        strippedString = strippedString[::-1]
    return strippedString


def random_upper(string):
    return "".join(
        random.choice((x, y)) for x, y in zip(string.upper(), string.lower())
    )
