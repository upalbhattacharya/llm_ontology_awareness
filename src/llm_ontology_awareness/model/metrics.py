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
