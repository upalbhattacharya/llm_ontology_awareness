#!/usr/bin/env python

"""(WIP) Sample selection for few-shot prompting"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

import polars as pl

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, help="DataFrame Dataset to load")
parser.add_argument(
    "-o", "--output_dir", type=str, help="Path to store generated output"
)
parser.add_argument("-m", "--metrics", type=str, help="Path to metrics dictionary")
parser.add_argument(
    "-k", "--count", type=int, default=2, help="Number of examples to select"
)

args = parser.parse_args()
key = "class_counts"

with open(args.metrics, "r") as f:
    metrics = json.load(f)

df = pl.read_ndjson(args.file)

# Select top 'k' classes to select samples from
selected_classes = list(
    k for k, v in sorted(metrics[key].items(), key=lambda x: x[1], reverse=True)
)[: args.count]

example_df = df.clear()
for cls in selected_classes:
    pool = df.join(example_df, on=df.columns, how="anti")
    example_df = pl.concat(
        [
            example_df,
            pool.filter(pool["Ranked List"].list.contains(cls)).sample(n=1, seed=47),
        ]
    )

df = df.join(example_df, on=df.columns, how="anti")

date_dir = datetime.now().strftime("%Y-%m-%d")
final_dir = args.output_dir
count = sum([x.startswith(date_dir) for x in os.listdir(args.output_dir)])
final_dir = (
    Path(final_dir) / f"{date_dir}.{count}"
    if count != 0
    else Path(final_dir) / date_dir
)
if not os.path.exists(final_dir):
    os.makedirs(final_dir)


df.write_ndjson(Path(final_dir) / "term_typing_ranked_retrieval_dataset.json")
example_df.write_ndjson(Path(final_dir) / "term_typing_ranked_retrieval_examples.json")
