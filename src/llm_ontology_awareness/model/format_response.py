#!/usr/bin/env python

import re

import polars as pl


def binary_classify(response) -> bool:
    value_map = {
        "true": True,
        "false": False,
    }
    pattern = re.compile(r"(true|false)", re.MULTILINE)
    return value_map.get(re.search(pattern, response).group(0))


format_types = {
    "binary_classify": {"function": binary_classify, "return_dtype": pl.Boolean}
}
