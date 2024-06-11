#!/usr/bin/env python3

"""Create targets for Ontology Individual to Concept mapping as a nested dictionary"""

import os
from typing import Optional

from ontology_awareness.ontology_processing import ontology_processing


def create_targets(in_file: str, out_dir: Optional[str] = None) -> None:
    onto = ontology_processing.OntologyProcessing(ontologyPath=in_file)
    print(onto.class_individuals)


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
        default=os.getcwd(),
    )
    args = parser.parse_args()
    print(args.file)
    print(args.output)
    create_targets(args.file, args.output)
