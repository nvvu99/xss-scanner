import re

from utils import strip


def generate_context_breaker(script: str, xss_checker: str) -> str:
    broken = script.split(xss_checker)
    pre = broken[0]
    #  remove everything that is between {..}, "..." or '...'
    pre = re.sub(r'(?s)\{.*?\}|(?s)\(.*?\)|(?s)".*?"|(?s)\'.*?\'', "", pre)
    breaker = ""
    num = 0
    for char in pre:  # iterate over the remaining characters
        if char == "{":
            breaker += "}"
        elif char == "(":
            # yes, it should be ); but we will invert the whole thing later
            breaker += ";)"
        elif char == "[":
            breaker += "]"
        elif char == "/":
            try:
                if pre[num + 1] == "*":
                    breaker += "/*"
            except IndexError:
                pass
        elif char == "}":
            # we encountered a } so we will strip off "our }" because this one does the job
            breaker = strip(breaker, "}")
        elif char == ")":
            # we encountered a ) so we will strip off "our }" because this one does the job
            breaker = strip(breaker, ")")
        elif breaker == "]":
            # we encountered a ] so we will strip off "our }" because this one does the job
            breaker = strip(breaker, "]")
        num += 1

    return breaker[::-1]  # invert the breaker string
