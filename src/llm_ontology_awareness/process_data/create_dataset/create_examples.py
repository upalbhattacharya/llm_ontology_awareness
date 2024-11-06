#!/usr/bin/env python

import polars as pl
import argparse


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
