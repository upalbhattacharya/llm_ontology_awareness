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

    from llm_ontology_awareness.model.open_ai.run_args import RunArguments

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--y_true", help="Path to true labels", type=str, required=True
    )
    parser.add_argument(
        "-p", "--y_pred", help="Path to prediction labels", type=str, required=True
    )
    parser.add_argument(
        "-r", "--run_args", help="Run arguments", type=str, required=True
    )
    args = parser.parse_args()

    with open(args.run_args, "r") as f:
        args_raw = f.read()
        run_args = RunArguments.parse_raw(args_raw)

    output_dir = os.path.dirname(args.y_pred)

    y_true = pl.read_ndjson(args.y_true)
    y_pred = pl.read_ndjson(args.y_pred)

    metrics = task_metrics[run_args.task_type](
        y_true.get_column("Member"), y_pred.get_column("Prediction")
    )
    with open(os.path.join(output_dir, "pred_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)
