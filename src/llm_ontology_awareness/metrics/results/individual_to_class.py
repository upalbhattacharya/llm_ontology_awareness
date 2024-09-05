#!/usr/bin/env python

import logging
from typing import Union

import polars as pl
from sklearn.metrics import accuracy_score, average_precision_score, confusion_matrix
from sklearn.metrics import precision_recall_fscore_support as prfs


def binary_classify(
    true_df: pl.DataFrame, pred_df: pl.DataFrame
) -> dict[float, float, float, Union[float, None]]:
    y_true = true_df["Member"]
    y_pred = pred_df["Prediction"]
    p, r, f, s = prfs(y_true, y_pred, average="binary")
    a = accuracy_score(y_true, y_pred)
    ap = average_precision_score(y_true, y_pred)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    spec = tn / (tn + fp)
    fnr = fn / (fn + tp)
    return {
        "precision": p,
        "recall": r,
        "specificity": spec,
        "fnr": fnr,
        "f1": f,
        "average_precision": ap,
        "accuracy": a,
        "support": s,
    }


if __name__ == "__main__":
    import argparse
    import json
    import os

    import polars as pl

    from llm_ontology_awareness.metrics.task_map import task_types

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-yt", "--y_true", help="Path to true labels", type=str, required=True
    )
    parser.add_argument(
        "-yp", "--y_pred", help="Path to prediction labels", type=str, required=True
    )
    parser.add_argument(
        "-o", "--ont_type", help="Ontology Task type", type=str, required=True
    )
    parser.add_argument("-n", "--task_type", help="Task type", type=str, required=True)
    args = parser.parse_args()

    output_dir = os.path.dirname(args.y_pred)

    y_true = pl.read_ndjson(args.y_true)
    y_pred = pl.read_ndjson(args.y_pred)

    try:
        metrics = task_types[args.task_type]["pred_metrics"](
            y_true.get_column("Member"), y_pred.get_column("Prediction")
        )
    except KeyError:
        logging.error(
            f"Argument `task_type` must be one of: {list(task_types.keys())}. Got value {args.task_type}"
        )

    with open(os.path.join(output_dir, "pred_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)
