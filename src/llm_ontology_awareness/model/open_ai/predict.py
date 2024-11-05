#!/usr/bin/env python
"""Prediction script for non-Batch API models"""

from typing import Dict, Union

import jsonlines
import polars as pl
from dotenv import load_dotenv
from llm_ontology_awareness.model.open_ai.datasets.term_typing import (
    TermTypingRankedRetrievalDataset,
)
from openai import OpenAI
from tqdm import tqdm

load_dotenv()


def predict(test_data, run_args, **kwargs) -> Union[Dict, pl.DataFrame]:

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    responses = []
    label_mapping = []
    num_samples = len(test_data)
    test_data = iter(test_data)
    for i in tqdm(range(num_samples)):
        inst, prompt, label = next(test_data)
        label_mapping.append((f"task-{i}", inst, label))
        completion = client.chat.completions.create(
            model=run_args.llm_name,
            max_completion_tokens=run_args.max_tokens,
            messages=prompt,
        )
        completion["custom_id"] = f"task-{i}"
        responses.append(completion)

    label_mapping_df = pl.DataFrame(
        label_mapping,
        schema=[
            ("Custom ID", str),
            ("Individual", str),
            ("Member", list[str]),
        ],
    )

    return label_mapping_df, responses


if __name__ == "__main__":
    import argparse
