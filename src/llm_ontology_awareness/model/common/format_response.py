#!/usr/bin/env python

import re

import polars as pl


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


def ranked_retrieval(response: str) -> list:
    rep_pat = ["<|eot_id|>", "[", "]"]
    replace_p = re.compile(f"(?:{ rep_pat.join("|")})")    
    ranks = list(filter(None, response.split("\n")))

    # Filter
    ranks = [

    ranks = [
        item.replace("[", "").replace("]", "")
        for item in ranks
        if re.match(r"^\d", item)
    ]

    pattern = re.compile(r"^\d+.*\s+(.*)", re.MULTILINE)
    items = [re.search(pattern, r).group(1) for r in ranks]
    return items
