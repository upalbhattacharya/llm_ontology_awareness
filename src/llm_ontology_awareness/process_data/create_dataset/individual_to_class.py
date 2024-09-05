#!/usr/bin/env python3

"""Create targets for Ontology Individual to Concept mapping as a nested dictionary"""

import argparse
import os
from datetime import datetime
from itertools import product
from pathlib import Path
from typing import Optional

import ontospy
import polars as pl


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split("=")
            getattr(namespace, self.dest)[key] = value


class ClassAssertionBinaryClassificationDataset:
    """Generate individual to class membership dataset"""

    def __init__(self, ontologyPath: str, **kwargs):
        self.model = ontospy.Ontospy(ontologyPath, hide_individuals=False)
        if kwargs.get("ancestry", None):
            self.ancestry = eval(kwargs["ancestry"])
            print(type(self.ancestry))

    def __call__(
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

        if self.ancestry:

            def check_ancestor(individual, cls, membership) -> bool:
                if cls in individual._instance_of:
                    membership.append(True)
                else:
                    membership.append(False)
                    for child_cls in cls.children():
                        check_ancestor(individual, child_cls, membership)

            entries_ancestry = []
            for ind, cl in product(
                list(self.model.all_individuals), list(self.model.all_classes)
            ):
                membership = []
                check_ancestor(ind, cl, membership)
                entries_ancestry.append((ind.locale, cl.locale, any(membership)))

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
            entries, schema=[("Individual", str), ("Class", str), ("Member", bool)]
        )

        df.write_ndjson(
            Path(final_dir) / "individual_direct_membership_binary_classify.json"
        )

        if self.ancestry:

            df = pl.DataFrame(
                entries_ancestry,
                schema=[("Individual", str), ("Class", str), ("Member", bool)],
            )

            df.write_ndjson(
                Path(final_dir) / "individual_ancestry_membership_binary_classify.json"
            )


class ClassAssertionRankedRetrievalDataset:
    """Generate individual to class membership dataset"""

    def __init__(self, ontologyPath: str, **kwargs):
        self.model = ontospy.Ontospy(ontologyPath, hide_individuals=False)

    def __call__(
        self,
        out_dir: Optional[str] = None,
    ) -> None:

        def get_ordered_ancestors(parents, membership) -> bool:
            membership.extend(
                [
                    cls.locale
                    for cls in sorted(parents, key=lambda x: x.locale)
                    if cls.locale not in membership
                ]
            )
            for parent in parents:
                get_ordered_ancestors(parent.parents(), membership)

        ranked_entries = []
        for ind in list(self.model.all_individuals):
            ranked_membership = []
            get_ordered_ancestors(ind._instance_of, ranked_membership)
            ranked_entries.append((ind.locale, ranked_membership))

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

        df.write_ndjson(
            Path(final_dir) / "class_assertion_ranked_retrieval_dataset.json"
        )


if __name__ == "__main__":
    import argparse

    from llm_ontology_awareness.metrics.task_map.individual_to_class import task_types

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
        "-t",
        "--task_type",
        help="Task type",
        type=str,
        default=None,
    )
    parser.add_argument(
        "-k",
        "--kwargs",
        nargs="*",
        help="Extra Named Arguments",
        action=ParseKwargs,
    )
    args = parser.parse_args()
    if args.output is None:
        args.output = Path(args.file).parents[0]

    if not args.kwargs:
        args.kwargs = {}

    if not task_types.get(args.task_type, None):
        raise KeyError(
            f"Argument `task_type` must be one of {list(task_types.keys())}. Found {args.task_type}"
        )

    itcd = task_types[args.task_type]["dataset"](ontologyPath=args.file, **args.kwargs)
    itcd(out_dir=args.output)
