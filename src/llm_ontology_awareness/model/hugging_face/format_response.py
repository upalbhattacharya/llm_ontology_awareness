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


format_types = {
    "binary_classify": {"function": binary_classify, "return_dtype": pl.Boolean}
}