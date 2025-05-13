#!/usr/bin/env python

import argparse
import glob
import json
import os

import polars as pl
from llm_ontology_awareness.model.open_ai.run_args import RunArguments
from llm_ontology_awareness.task_map.term_typing import task_types

parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--response_file_dir",
    help="Response objects directory",
    type=str,
    required=True,
)
parser.add_argument(
    "-r",
    "--run_args",
    help="Run arguments",
    type=str,
    required=True,
)
parser.add_argument(
    "-l",
    "--label_mapping",
    type=str,
    help="Label mapping file to align responses based on Custom ID",
    required=True,
)

args = parser.parse_args()
with open(args.run_args, "r") as f:
    args_raw = f.read()
    run_args = RunArguments.parse_raw(args_raw)

output_dir = args.response_file_dir
path_glob = f"{args.response_file_dir}/batch_output_*.jsonl"
batch_output_files = glob.glob(path_glob)
results = []

# Create Prediction DataFrame
for batch_output_path in batch_output_files:
    with open(batch_output_path, "r") as f:
        for line in f:
            json_object = json.loads(line.strip())
            results.append(
                (
                    json_object["custom_id"],
                    json_object["response"]["body"]["choices"][0]["embedding"],
                )
            )

df = pl.DataFrame(results, schema=[("Custom ID", str), ("Response", str)])

y_true_df = pl.read_ndjson(args.label_mapping)

join_df = df.join(y_true_df, on="Custom ID")
print(join_df)
columns = task_types[run_args.task_type]["format_response"]["df_columns"]
columns.append("Response")
print(columns)
join_df = join_df.select(columns)
join_df = join_df.with_columns(
    pl.col("Response")
    .map_elements(
        # function=task_types[run_args.task_type]["format_response"]["function"],
        # return_dtype=task_types[run_args.task_type]["format_response"]["return_dtype"],
        function=lambda x: task_types[run_args.task_type]["format_response"][
            "function"
        ](x, run_args.llm_name),
        return_dtype=task_types[run_args.task_type]["format_response"]["return_dtype"],
    )
    .alias("Prediction")
)
print(join_df)

join_df.write_ndjson(os.path.join(output_dir, "predictions.json"))
