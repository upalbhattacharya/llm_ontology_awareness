#!/usr/bin/env python

import re

import polars as pl

# Response formatting for different models


def llama3(value: str):

    values = re.sub(
        r"(<\|begin_of_text\|>\s*|<\|eot_id\|>)", "", value
    )  # For older response format
    offset = values.find("<|start_header_id|>assistant<|end_header_id|>")
    if offset != -1:
        values = values[offset + len("<|start_header_id|>assistant<|end_header_id|>") :]
    values = re.sub(
        r"^.+?:", "", values, re.DOTALL
    )  # Removes non-essential starting text
    values = re.sub(r"\b\d+\b", "", values)  # Remove numbers
    values = re.sub(
        r"('|,|\[|\]|\.|\*)", "", values
    )  # Remove other special demarcation characters
    values = re.sub(
        r"\s+", " ", values
    )  # Replace all extra blank spaces/newlines with single spaces
    values = list(filter(None, values.split()))
    return values


def deepseekr1(value: str):
    # values = re.sub(r"^.*</think>", "", value, re.DOTALL)
    offset = value.find("</think>")
    print(offset)
    values = value[offset + 8 :]
    print(values)
    print("-" * 40)
    values = llama3(values)
    return values


def gpt_4o(value: str):
    values = value
    return values


llm_response_extract = {
    "meta-llama/Meta-Llama-3-8B-Instruct": llama3,
    "deepseek-ai/DeepSeek-R1-Distill-Llama-8B": deepseekr1,
    "gpt-4o": llama3,
    "o1-preview": llama3,
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
    # assistant_response = llm_response_extract[llm_name](response)
    items = llm_response_extract[llm_name](response)
    # ranks = list(filter(None, assistant_response.split("\n")))
    # ranks = [re.sub(r"[[']]", "", item).strip() for item in ranks]
    # ranks = [item for item in ranks if re.match(r"^\d", item)]

    # pattern = re.compile(r"(^\d+)?.*\s+(.*)", re.MULTILINE)
    # items = [re.search(pattern, r).group(2) for r in ranks]
    return items
