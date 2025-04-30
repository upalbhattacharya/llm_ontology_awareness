#!/usr/bin/env python

import argparse
import glob
import json
import os
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

parser = argparse.ArgumentParser()
parser.add_argument(
    "-b",
    "--batch_file_dir",
    help="Directory containing batch_files",
    type=str,
    required=True,
)
args = parser.parse_args()
path_glob = f"{args.batch_file_dir}/*.jsonl"
batch_files = glob.glob(path_glob)
id_dict = defaultdict(list)
# Upload batch input
for batch_file_path in batch_files:
    batch_file = client.files.create(file=open(batch_file_path, "rb"), purpose="batch")
    id_dict["batch_file_id"].append(batch_file.id)
    print(batch_file_path)

    # Submit batch job
    submit_batch = client.batches.create(
        input_file_id=batch_file.id,
        endpoint="/v1/embeddings",
        completion_window="24h",
        metadata={
            "description": batch_file_path,
        },
    )

    id_dict["batch_job_id"].append(submit_batch.id)

with open(os.path.join(args.batch_file_dir, "ids.json"), "w") as f:
    json.dump(id_dict, f, indent=4)
