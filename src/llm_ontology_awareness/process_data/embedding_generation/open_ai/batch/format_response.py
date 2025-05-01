#!/usr/bin/env python

import argparse
import glob
import json
import os

import polars as pl

parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--response_file_dir",
    help="Response objects directory",
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

output_dir = args.response_file_dir
path_glob = f"{args.response_file_dir}/embedding_batch_output_*.jsonl"
batch_output_files = glob.glob(path_glob)
results = []

for batch_output_path in batch_output_files:
    with open(batch_output_path, "r") as f:
        for line in f:
            json_object = json.loads(line.strip())
            results.append(
                (
                    json_object["custom_id"],
                    json_object["response"]["body"]["data"][0]["embedding"],
                )
            )

df = pl.DataFrame(
    results, schema=[("Custom ID", str), ("Embedding", pl.Array(pl.Float64, 3072))]
)
y_true_df = pl.read_ndjson(args.label_mapping)
print(y_true_df)
join_df = df.join(y_true_df, on="Custom ID")
columns = ["Entity Label", "Embedding"]
join_df = join_df.select(columns)

print(join_df)
join_df.write_ndjson(os.path.join(output_dir, "embeddings.json"))
