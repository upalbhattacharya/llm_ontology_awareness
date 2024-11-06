#!/usr/bin/env python

import polars as pl
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "-file", type=str,
                    help="DataFrame Dataset to load")
parser.add_argument("-o", "--output_dir", type=str,
                    help="Path to store generated output")
parser.add_argument("-m", "--metrics", type=str,
                    help="Path to metrics dictionary")

args = parser.parse_args()

key = "class_counts"


        date_dir = datetime.now().strftime("%Y-%m-%d")
        final_dir = out_dir
        count = sum([x.startswith(date_dir) for x in os.listdir(out_dir)])
        final_dir = (
            Path(final_dir) / f"{date_dir}.{count}"
            if count != 0
            else Path(final_dir) / date_dir
        )
        if not os.path.exists(final_dir):
            os.makedirs(final_dir)

        df = pl.DataFrame(
            ranked_entries,
            schema=[("Individual", str), ("Ranked List", list[str])],
        )

        df.write_ndjson(Path(final_dir) / "term_typing_ranked_retrieval_dataset.json")
