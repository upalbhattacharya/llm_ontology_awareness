#!/usr/bin/env python

import argparse
import json
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d",
    "--dir",
    help="Directory to look through json files to make dictionary",
    type=str,
    required=True,
)
parser.add_argument(
    "-o",
    "--output",
    help="Directory to write generated dictionary to",
    type=str,
    required=True,
)

args = parser.parse_args()
run_args_files = [
    f
    for f in os.listdir(args.dir)
    if re.search(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}.json", f
    )
]

summary_dict = {}

for run_args_file in run_args_files:
    with open(os.path.join(args.dir, run_args_file), "r") as f:
        d = json.load(f)
        summary_dict[os.path.splitext(run_args_file)[0]] = d["description"]

with open(os.path.join(args.output, "run_args_summary.json"), "w") as f:
    json.dump(summary_dict, f, indent=4)
