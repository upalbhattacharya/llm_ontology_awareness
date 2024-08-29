#!/usr/bin/env python

from typing import Union

from sklearn.metrics import accuracy_score, average_precision_score, confusion_matrix
from sklearn.metrics import precision_recall_fscore_support as prfs


def binary_classify(
    y_true: list, y_pred: list
) -> dict[float, float, float, Union[float, None]]:
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


task_metrics = {
    "binary_classify": binary_classify,
}


if __name__ == "__main__":
    import argparse
    import json
    import os

    import polars as pl

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--y_true", help="Path to true labels", type=str, required=True
    )
    parser.add_argument(
        "-p", "--y_pred", help="Path to prediction labels", type=str, required=True
    )
    parser.add_argument("-t", "--task_type", help="Task type", type=str, required=True)
    args = parser.parse_args()

    output_dir = os.path.dirname(args.y_pred)

    y_true = pl.read_ndjson(args.y_true)
    y_pred = pl.read_ndjson(args.y_pred)

    print(y_pred["Prediction"].unique())

    metrics = task_metrics[args.task_type](
        y_true.get_column("Member"), y_pred.get_column("Prediction")
    )
    with open(os.path.join(output_dir, "pred_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)
