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
output_dir = os.path.dirname(args.job_dict)

with open(args.job_dict, "r") as f:
    ids = json.load(f)

responses = [client.batches.retrieve(idx) for idx in ids["batch_job_id"]]

if not all([r.status == "completed" for r in responses]):
    incomplete_jobs = list(filter(lambda y: y.status != "completed", responses))
    print(f"{len(incomplete_jobs)}/{len(responses)} jobs completed")
    print(incomplete_jobs)
else:
    for i, response in enumerate(responses):
        output_file_id = response.output_file_id
        file_response = client.files.content(output_file_id).content

        with open(
            os.path.join(output_dir, f"embedding_batch_output_{i+1}.jsonl"), "wb"
        ) as f:
            f.write(file_response)
