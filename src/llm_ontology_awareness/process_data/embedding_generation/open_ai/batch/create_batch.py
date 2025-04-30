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


def create_embedding_batch(
    run_args: RunArguments, **kwargs
) -> (list[dict], pl.DataFrame):
    model = ontospy.Ontospy(run_args.input, hide_individuals=False)

    tasks = []
    label_mapping = []

    if run_args.entities == "concepts":
        entities = [ent.locale for ent in model.all_classes]
    elif run_args.entities == "individuals":
        entities = [ent.locale for ent in model.all_individuals]
    else:
        raise Exception(f"Entity type {run_args.entities} not defined")

    for i, ent_name in tqdm(range(len(entities))):
        task = {
            "custom_id": f"embedding_task-{i}",
            "method": "POST",
            "url": "/v1/embeddings",
            "body": {
                "model": run_args.llm_name,
                "messages": messages,
                "max_completion_tokens": run_args.max_tokens,
                "temperature": run_args.temperature,
            },
        }
