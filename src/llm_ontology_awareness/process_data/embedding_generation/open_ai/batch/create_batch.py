#!/usr/bin/env python

import ontospy
import polars as pl
from llm_ontology_awareness.model.open_ai.datasets.term_typing import (
    TermTypingRankedRetrievalDataset,
)
from llm_ontology_awareness.process_data.embedding_generation.open_ai.run_args import (
    RunArguments,
)
from tqdm import tqdm


def create_embedding_batch(run_args: RunArguments, **kwargs) -> (pl.DataFrame, dict):
    model = ontospy.Ontospy(run_args.input, hide_individuals=False)

    tasks = []
    label_mapping = []
