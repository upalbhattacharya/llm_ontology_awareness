#!/usr/bin/env python

import llm_ontology_awareness.metrics.datasets.individual_to_class as dataset_metrics
import llm_ontology_awareness.metrics.results.individual_to_class as pred_metrics
from llm_ontology_awareness.process_data.create_dataset.individual_to_class import (
    ClassAssertionBinaryClassificationDataset,
    ClassAssertionRankedRetrievalDataset,
)

task_types = {
    "binary_classify": {
        "dataset": ClassAssertionBinaryClassificationDataset,
        "dataset_metrics": dataset_metrics.ClassAssertionBinaryClassification,
        "pred_metrics": pred_metrics.binary_classify,
    },
    "ranked_retrieval": {
        "dataset": ClassAssertionRankedRetrievalDataset,
        "dataset_metrics": dataset_metrics.ClassAssertionRankedRetrieval,
        "pred_metrics": pred_metrics.binary_classify,
    },
}
