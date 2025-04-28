#!/usr/bin/env python

import polars as pl
from llm_ontology_awareness.model.open_ai.datasets.term_typing import (
    TermTypingRankedRetrievalDataset,
)
from llm_ontology_awareness.process_data.embedding_generation.open_ai.run_args import (
    RunArguments,
)
from tqdm import tqdm


def create_embedding_batch(test_data, run_args, **kwargs) -> (pl.DataFrame, dict):
    tasks = []
    label_mapping = []
    num_samples = len(test_data)
    test_data = iter(test_data)
