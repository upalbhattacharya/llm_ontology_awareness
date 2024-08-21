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

print(ids)

response = client.batches.retrieve(ids["batch_job_id"])
if response.status != "completed":
    print(response)
