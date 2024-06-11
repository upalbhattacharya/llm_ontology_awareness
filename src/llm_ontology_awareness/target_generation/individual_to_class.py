#!/usr/bin/env python3

"""Create targets for Ontology Individual to Concept mapping as a nested dictionary"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

from llm_ontology_awareness.ontology_processing import ontology_processing


class IndividualToClassTargets:
    def __init__(self):
        pass

    def get_individual_classes(
        self,
        in_file: str,
        out_dir: Optional[str] = None,
        save: Optional[bool] = True,
        date_dir: Optional[bool] = True,
    ) -> dict[list]:
        onto = ontology_processing.OntologyProcessing(ontologyPath=in_file)
        class_individuals = onto.class_individuals
        individual_classes = {}
        for k, v in class_individuals.items():
            for x in v:
                individual_classes.setdefault(x, []).append(k)

        df = pd.DataFrame.from_dict(individual_classes, orient="index")

        final_dir = out_dir

        if save:
            if date_dir:
                date_dir = datetime.now().strftime("%Y-%m-%d")
                count = sum([x.startswith(date_dir) for x in os.listdir(out_dir)])
                final_dir = (
                    Path(final_dir) / f"{date_dir}.{count}"
                    if count != 0
                    else Path(final_dir) / date_dir
                )
                if not os.path.exists(final_dir):
                    os.makedirs(final_dir)

            with open(Path(final_dir) / "individual_classes.json", "w") as f:
                json.dump(individual_classes, indent=4, fp=f)

            df.to_csv(Path(final_dir) / "individual_classes.csv")

        return individual_classes


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

    parser.add_argument(
        "-s",
        "--save",
        help="Whether to save generated mapping",
        type=bool,
        default=True,
    )
    parser.add_argument(
        "-d",
        "--date_dir",
        help="Create date directory (help with versioning)",
        type=bool,
        default=True,
    )
    args = parser.parse_args()
    if args.output is None:
        args.output = Path(args.file).parents[0]

    target_gen = IndividualToClassTargets()
    target_gen.get_individual_classes(
        in_file=args.file,
        out_dir=args.output,
        save=args.save,
        date_dir=args.date_dir,
    )
