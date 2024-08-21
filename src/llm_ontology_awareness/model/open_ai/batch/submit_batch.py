#!/usr/bin/env python

import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

parser = argparse.ArgumentParser()
parser.add_argument(
    "-b",
    "--batch_file",
    help="Path to batch tasks file",
    type=str,
    required=True,
)
args = parser.parse_args()
output_dir = os.path.dirname(args.batch_file)

# Upload batch input
batch_file = client.files.create(file=open(args.batch_file, "rb"), purpose="batch")

id_dict = {
    "batch_file_id": batch_file.id,
}

# Submit batch
submit_batch = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
        "description": output_dir,
    },
)
print(submit_batch)

id_dict["batch_job_id"] = submit_batch.id

with open(os.path.join(output_dir, "ids.json"), "w") as f:
    json.dump(id_dict, f, indent=4)
