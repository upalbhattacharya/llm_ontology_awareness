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
    "-j",
    "--job_dict",
    help="Path to json object with IDs",
    type=str,
    required=True,
)
args = parser.parse_args()

with open(args.job_dict, "r") as f:
    ids = json.load(f)

response = client.batches.retrieve(ids["batch_job_id"])
if response.status != "completed":
    print(response)
else:
    output_dir = os.path.dirname(args.job_dict)
    output_file_id = response.output_file_id
    file_response = client.files.content(output_file_id).content

    with open(os.path.join(output_dir, "batch_output.jsonl"), "wb") as f:
        f.write(file_response)
