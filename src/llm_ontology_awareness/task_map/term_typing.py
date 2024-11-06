#!/usr/bin/env python

import llm_ontology_awareness.metrics.datasets.term_typing as dataset_metrics
import llm_ontology_awareness.metrics.results.term_typing as pred_metrics
import polars as pl
from llm_ontology_awareness.model.common import format_response

task_types = {
    "binary_classify": {
        "dataset_metrics": dataset_metrics.TermTypingBinaryClassification,
        "pred_metrics": pred_metrics.binary_classify,
        "format_response": {
            "function": format_response.binary_classify,
            "return_dtype": pl.Boolean,
            "df_columns": ["Individual", "Class"],
        },
    },
    "ranked_retrieval": {
        "dataset_metrics": dataset_metrics.TermTypingRankedRetrieval,
        "pred_metrics": pred_metrics.ranked_retrieval,
        "format_response": {
            "function": format_response.ranked_retrieval,
            "return_dtype": pl.List(pl.String),
            "df_columns": ["Individual"],
        },
    },
}
