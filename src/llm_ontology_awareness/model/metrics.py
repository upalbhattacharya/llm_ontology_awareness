#!/usr/bin/env python

from typing import Union

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support as prfs


def binary_classify(
    y_true: list, y_pred: list
) -> dict[float, float, float, Union[float, None]]:
    p, r, f, s = prfs(y_true, y_pred, average="binary")
    a = accuracy_score(y_true, y_pred)
    return {
        "precision": p,
        "recall": r,
        "f1": f,
        "accuracy": a,
        "support": s,
    }


task_metrics = {
    "binary_classify": binary_classify,
}
