#!/usr/bin/env python

import polars as pl

import llm_ontology_awareness.metrics.datasets.term_typing as dataset_metrics
import llm_ontology_awareness.metrics.results.term_typing as pred_metrics
from llm_ontology_awareness.model.common import format_response
from llm_ontology_awareness.process_data.create_dataset.term_typing import (
    TermTypingBinaryClassificationDataset,
    TermTypingRankedRetrievalDataset,
)

task_types = {
    "binary_classify": {
        "dataset": TermTypingBinaryClassificationDataset,
        "dataset_metrics": dataset_metrics.TermTypingBinaryClassification,
        "pred_metrics": pred_metrics.binary_classify,
        "format_response": {
            "function": format_response.binary_classify,
            "return_dtype": pl.Boolean,
            "df_columns": ["Individual", "Class"],
        },
    },
    "ranked_retrieval": {
        "dataset": TermTypingRankedRetrievalDataset,
        "dataset_metrics": dataset_metrics.TermTypingRankedRetrieval,
        "pred_metrics": pred_metrics.ranked_retrieval,
        "format_response": {
            "function": format_response.ranked_retrieval,
            "return_dtype": pl.List(pl.String),
            "df_columns": ["Individual"],
        },
    },
}
