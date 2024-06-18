#!/usr/bin/env python

from sklearn.metrics import precision_recall_fscore_support as prfs


def binary_classify(
    y_true: list, y_pred: list
) -> dict[float, float, float, None | float]:
    p, r, f, s = prfs(y_true, y_pred, average="binary")
    return {
        "precision": p,
        "recall": r,
        "f1": f,
        "support": s,
    }


task_metrics = {
    "binary_classify": binary_classify,
}
