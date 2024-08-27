#!/usr/bin/env python3

"""Create targets for Ontology Individual to Concept mapping as a nested dictionary"""

import os
from datetime import datetime
from itertools import product
from pathlib import Path
from typing import Optional

import ontospy
import polars as pl


class IndividualToClassDataset:
    """Generate individual to class membership dataset"""

    def __init__(self, ontologyPath: str):
        self.model = ontospy.Ontospy(ontologyPath, hide_individuals=False)

    def individual_direct_membership_binary_classify(
        self,
        out_dir: Optional[str] = None,
    ) -> None:

        entries = [
            (
                ind.locale,
                cl.locale,
                cl.locale in map(lambda x: x.locale, ind._instance_of),
            )
            for (ind, cl) in product(
                list(self.model.all_individuals), list(self.model.all_classes)
            )
        ]
        df = pl.DataFrame(
            entries, schema=[("Individual", str), ("Class", str), ("Member", bool)]
        )
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

        df.write_ndjson(
            Path(final_dir) / "individual_direct_membership_binary_classify.json"
        )


if __name__ == "__main__":
    import argparse

    # Get input and output files
    parser = argparse.ArgumentParser(
        description="Create targets for ontology Individual to Concept mapping as a nested dictionary"
    )
    parser.add_argument(
        "-f", "--file", help="Ontology file to input", type=str, required=True
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Directory to save to. Defaults to present directory",
        type=str,
        default=None,
    )
    args = parser.parse_args()
    if args.output is None:
        args.output = Path(args.file).parents[0]

    itcd = IndividualToClassDataset(ontologyPath=args.file)
    itcd.individual_direct_membership_binary_classify(out_dir=args.output)
