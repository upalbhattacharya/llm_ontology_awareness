#!/usr/bin/env python

import argparse
import json
import os

import polars as pl
from dotenv import load_dotenv
from openai import OpenAI

from llm_ontology_awareness.model.common.format_response import format_types
from llm_ontology_awareness.model.open_ai.run_args import RunArguments

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

parser = argparse.ArgumentParser()
parser.add_argument(
    "-j",
    "--job_dict",
    help="Path to json object with IDs",
    type=str,
    required=True,
)
parser.add_argument(
    "-r",
    "--run_args",
    help="Run arguments",
    type=str,
    default=True,
)
args = parser.parse_args()

with open(args.run_args, "r") as f:
    args_raw = f.read()
    run_args = RunArguments.parse_raw(args_raw)

with open(args.job_dict, "r") as f:
    ids = json.load(f)

print(ids)

response = client.batches.retrieve(ids["batch_job_id"])
if response.status != "completed":
    print(response)
else:
    output_dir = os.path.dirname(args.job_dict)
    output_file_id = response.output_file_id
    file_response = client.files.content(output_file_id).content

    with open(os.path.join(output_dir, "batch_output.jsonl"), "wb") as f:
        f.write(file_response)

    # Create Prediction DataFrame
    results = []
    with open(os.path.join(output_dir, "batch_output.jsonl"), "r") as f:
        for line in f:
            json_object = json.loads(line.strip())
            results.append(
                (
                    json_object["custom_id"],
                    json_object["response"]["body"]["choices"][0]["message"]["content"],
                )
            )

    df = pl.DataFrame(results, schema=[("Custom ID", str), ("Response", str)])

    y_true_df = pl.read_ndjson(os.path.join(output_dir, "label_mapping.json"))

    join_df = df.join(y_true_df, on="Custom ID")
    join_df = join_df.select(["Individual", "Class", "Response"])
    join_df = join_df.with_columns(
        pl.col("Response")
        .map_elements(
            function=format_types[run_args.task_type]["function"],
            return_dtype=format_types[run_args.task_type]["return_dtype"],
        )
        .alias("Prediction")
    )

    join_df.write_ndjson(os.path.join(output_dir, "responses.json"))
