from .format import is_escaped, random_upper, strip
from .extract import extract_scripts


def is_bad_context(position: int, non_executable_contexts: list):
    badContext = ""
    for each in non_executable_contexts:
        if each[0] < position < each[1]:
            badContext = each[2]
            break
    return badContext
