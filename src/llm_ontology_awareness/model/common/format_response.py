#!/usr/bin/env python

import re

import polars as pl

llm_split_string = {
    "meta-llama/Meta-Llama-3-8B-Instruct": re.compile(
        r".*<|start_header_id|>assistant<|end_header_id|>(.*)<|eot_id|>", re.DOTALL
    )
}


def binary_classify(response: str) -> bool:
    value_map = {
        "true": True,
        "false": False,
    }
    pattern = re.compile(r"(true|false)", re.MULTILINE)
    search_value = re.search(pattern, response.lower())

    return (
        value_map.get(search_value.group(0), None) if search_value is not None else None
    )


def ranked_retrieval(response: str, llm_name: str) -> list:
    # assistant_response = response.split(llm_split_string[llm_name])[-1]
    # assistant_response = llm_split_string[llm_name].search(response).group(1)
    assistant_response = re.search(
        r"<\|start_header_id\|>assistant<\|end_header_id\|>(.*)<\|eot_id\|>",
        response,
        flags=re.DOTALL,
    ).group(1)
    print(assistant_response)
    print("=" * 40)
    ranks = list(filter(None, assistant_response.split("\n")))
    ranks = [re.sub(r"[[']]", "", item).strip() for item in ranks]
    ranks = [item for item in ranks if re.match(r"^\d", item)]

    pattern = re.compile(r"(^\d+)?.*\s+(.*)", re.MULTILINE)
    items = [re.search(pattern, r).group(2) for r in ranks]
    return items
