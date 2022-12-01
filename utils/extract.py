import re


def extract_scripts(html_content: str, xss_checker: str):
    scripts = []
    matches = re.findall(r"(?s)<script.*?>(.*?)</script>", html_content.lower())
    for match in matches:
        if xss_checker in match:
            scripts.append(match)
    return scripts
