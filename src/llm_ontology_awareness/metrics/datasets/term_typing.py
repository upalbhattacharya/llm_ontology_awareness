#!/usr/bin/env python

import json
import os
from collections import Counter, defaultdict
from typing import Dict

import ontospy
import polars as pl


class TermTypingBinaryClassification:

    def __init__(self, data_path, ontology_path):
        self.data = pl.read_ndjson(data_path)
        self.ontology = ontospy.Ontospy(ontology_path, hide_individuals=False)

    def entity_counts(self) -> Dict[str, int]:
        counts = {
            "individuals": self.data["Individual"].unique().len(),
            "classes": self.data["Class"].unique().len(),
        }
        return counts

    def individual_counts(self) -> Dict[str, float]:
        ind_counts = dict(
            self.data.filter(pl.col("Member") is True)["Individual"]
            .value_counts()
            .iter_rows()
        )
        ind_counts = {
            k: v
            for k, v in sorted(ind_counts.items(), key=lambda x: x[1], reverse=True)
        }
        return ind_counts

    def class_counts(self) -> Dict[str, float]:
        class_counts = dict(
            self.data.filter(pl.col("Member") is True)["Class"]
            .value_counts()
            .iter_rows()
        )
        class_counts = {
            k: v
            for k, v in sorted(class_counts.items(), key=lambda x: x[1], reverse=True)
        }
        return class_counts

    def ontology_breadth(self) -> Dict[str, int]:
        level_cardinality = {}
        top_classes = self.ontology.toplayer_classes
        classes = top_classes
        level = 0
        while classes:
            level_cardinality[level] = len(classes)
            classes = [
                child
                for cls in classes
                for child in cls.children()
                if cls.children() != []
            ]
            level = level + 1
        return level_cardinality

    def ontology_dispersion(self) -> Dict[str, int]:
        dispersion = {cl.locale: len(cl.children()) for cl in self.ontology.all_classes}

        dispersion = {
            k: v
            for k, v in sorted(dispersion.items(), key=lambda x: x[1], reverse=True)
        }

        return dispersion

    def ontology_depth(self) -> Dict[str, int]:
        class_depth = defaultdict(int)
        top_classes = self.ontology.toplayer_classes

        def get_depth(present_depth, cls, depth_dict):
            depth_dict[cls.locale] = present_depth + 1
            if cls.children():
                for child in cls.children():
                    get_depth(present_depth + 1, child, depth_dict)
            else:
                return

        for cls in top_classes:
            get_depth(-1, cls, class_depth)

        class_depth = {k: v for k, v in sorted(class_depth.items(), key=lambda x: x[1])}

        return class_depth

    def label_counts(self) -> Dict[str, Dict[str, float]]:
        counts = dict(self.data["Member"].value_counts().iter_rows())
        return counts

    def __call__(self) -> Dict:
        metrics = defaultdict()
        metrics["entity_counts"] = self.entity_counts()
        metrics["class_counts"] = self.class_counts()
        metrics["individual_counts"] = self.individual_counts()
        metrics["ontology_depth"] = self.ontology_depth()
        metrics["ontology_breadth"] = self.ontology_breadth()
        metrics["ontology_dispersion"] = self.ontology_dispersion()
        metrics["label_counts"] = self.label_counts()

        return metrics


class TermTypingRankedRetrieval:

    def __init__(self, data_path, ontology_path):
        self.data = pl.read_ndjson(data_path)
        self.ontology = ontospy.Ontospy(ontology_path, hide_individuals=False)

    def entity_counts(self) -> Dict[str, int]:
        counts = {
            "individuals": len(self.ontology.all_individuals),
            "classes": len(self.ontology.all_classes),
        }
        return counts

    def individual_counts(self) -> Dict[str, float]:
        ind_dict = dict(self.data.iter_rows())
        ind_counts = {
            k: len(v)
            for k, v in sorted(ind_dict.items(), key=lambda x: len(x[1]), reverse=True)
        }
        return ind_counts

    def class_counts(self) -> Dict[str, float]:
        class_list = [
            cls for ranked in self.data["Ranked List"].to_list() for cls in ranked
        ]
        class_counts = dict(Counter(class_list))
        class_counts = {
            k: v
            for k, v in sorted(class_counts.items(), key=lambda x: x[1], reverse=True)
        }
        return class_counts

    def ontology_breadth(self) -> Dict[str, int]:
        level_cardinality = {}
        top_classes = self.ontology.toplayer_classes
        classes = top_classes
        level = 0
        while classes:
            level_cardinality[level] = len(classes)
            classes = [
                child
                for cls in classes
                for child in cls.children()
                if cls.children() != []
            ]
            level = level + 1
        return level_cardinality

    def ontology_dispersion(self) -> Dict[str, int]:
        dispersion = {cl.locale: len(cl.children()) for cl in self.ontology.all_classes}

        dispersion = {
            k: v
            for k, v in sorted(dispersion.items(), key=lambda x: x[1], reverse=True)
        }

        return dispersion

    def ontology_depth(self) -> Dict[str, int]:
        class_depth = defaultdict(int)
        top_classes = self.ontology.toplayer_classes

        def get_depth(present_depth, cls, depth_dict):
            depth_dict[cls.locale] = present_depth + 1
            if cls.children():
                for child in cls.children():
                    get_depth(present_depth + 1, child, depth_dict)
            else:
                return

        for cls in top_classes:
            get_depth(-1, cls, class_depth)

        class_depth = {k: v for k, v in sorted(class_depth.items(), key=lambda x: x[1])}

        return class_depth

    def __call__(self) -> Dict:
        metrics = defaultdict()
        metrics["entity_counts"] = self.entity_counts()
        metrics["class_counts"] = self.class_counts()
        metrics["individual_counts"] = self.individual_counts()
        metrics["ontology_depth"] = self.ontology_depth()
        metrics["ontology_breadth"] = self.ontology_breadth()
        metrics["ontology_dispersion"] = self.ontology_dispersion()

        return metrics


if __name__ == "__main__":
    import argparse

    from llm_ontology_awareness.task_map.term_typing import task_types

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_path", help="Path to Data DataFrame")
    parser.add_argument("-o", "--ontology_path", help="Path to ontology file")
    parser.add_argument(
        "-m", "--metrics_dir", help="Directory to save generated metrics"
    )
    parser.add_argument("-t", "--task_type", help="Task type", type=str, required=True)
    args = parser.parse_args()

    if not task_types.get(args.task_type, None):
        raise KeyError(
            f"`task_type` must be one of {list(task_types.keys())}. Found {args.task_type}"
        )
    itc_obj = task_types[args.task_type]["dataset_metrics"](
        data_path=args.data_path, ontology_path=args.ontology_path
    )
    metrics = itc_obj()

    with open(os.path.join(args.metrics_dir, "dataset_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)
