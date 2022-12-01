import re
from types import FunctionType
from typing import Optional
from utils import is_escaped, extract_scripts, is_bad_context


def parse_context(
    html_content: str,
    xss_checker: str,
    encoding: Optional[FunctionType] = None,
) -> dict:
    if encoding:
        html_content = html_content.replace(encoding(xss_checker), xss_checker)
    reflections = html_content.count(xss_checker)
    position_and_context = {}
    environment_details = {}
    clean_html_content = re.sub(r"<!--[.\s\S]*?-->", "", html_content)
    script_checkable = clean_html_content

    # Parse script contexts
    for script in extract_scripts(script_checkable, xss_checker):
        script_contexts = re.finditer(f"({xss_checker}.*?)$", script) or []
        for occurence in script_contexts:
            position = occurence.start(1)
            position_and_context[position] = "script"
            environment_details[position] = {"details": {"quote": ""}}
            reflection = occurence.group()
            for index, current_char in enumerate(reflection):
                if current_char in ("/", "'", "`", '"') and not is_escaped(
                    index, reflection
                ):
                    environment_details[position]["details"]["quote"] = current_char
                elif current_char in (")", "]", "}") and not is_escaped(
                    index, reflection
                ):
                    break
            script_checkable = script_checkable.replace(xss_checker, "", 1)

    # Parse attribute contexts
    if len(position_and_context) < reflections:
        attribute_contexts = re.finditer(
            f"<[^>]*?({xss_checker})[^>]*?>",
            clean_html_content,
        )
        for occurence in attribute_contexts:
            match = occurence.group(0)
            current_position = occurence.start(1)
            parts = re.split(r"\s", match)
            tag = parts[0][1:]
            for part in parts:
                if xss_checker in part:
                    Type, quote, name, value = "", "", "", ""
                    if "=" in part:
                        quote = re.search(r'=([\'`"])?', part).group(1)
                        name_and_value = part.split("=")[0], "=".join(
                            part.split("=")[1:]
                        )
                        if xss_checker == name_and_value[0]:
                            Type = "name"
                        else:
                            Type = "value"
                        name = name_and_value[0]
                        value = (
                            name_and_value[1].rstrip(">").rstrip(quote).lstrip(quote)
                        )
                    else:
                        Type = "flag"
                    position_and_context[current_position] = "attribute"
                    environment_details[current_position] = {}
                    environment_details[current_position]["details"] = {
                        "tag": tag,
                        "type": Type,
                        "quote": quote,
                        "value": value,
                        "name": name,
                    }

    # Parse html context
    if len(position_and_context) < reflections:
        html_contexts = re.finditer(xss_checker, clean_html_content)
        for occurence in html_contexts:
            current_position = occurence.start()
            if current_position not in position_and_context:
                position_and_context[occurence.start()] = "html"
                environment_details[current_position] = {}
                environment_details[current_position]["details"] = {}

    # Parse comment context
    if len(position_and_context) < reflections:
        comment_contexts = re.finditer(
            f"<!--[\\s\\S]*?({xss_checker})[\\s\\S]*?-->", html_content
        )
        for occurence in comment_contexts:
            current_position = occurence.start(1)
            position_and_context[current_position] = "comment"
            environment_details[current_position] = {}
            environment_details[current_position]["details"] = {}
    database = {}
    for i in sorted(position_and_context):
        database[i] = {}
        database[i]["position"] = i
        database[i]["context"] = position_and_context[i]
        database[i]["details"] = environment_details[i]["details"]

    bad_contexts = re.finditer(
        f"(?s)(?i)<(style|template|textarea|title|noembed|noscript)>[.\\s\\S]*({xss_checker})[.\\s\\S]*</\\1>",
        html_content,
    )
    non_executable_contexts = []
    for each in bad_contexts:
        non_executable_contexts.append([each.start(), each.end(), each.group(1)])

    if non_executable_contexts:
        for key in database.keys():
            position = database[key]["position"]
            badTag = is_bad_context(position, non_executable_contexts)
            if badTag:
                database[key]["details"]["badTag"] = badTag
            else:
                database[key]["details"]["badTag"] = ""
    return database
