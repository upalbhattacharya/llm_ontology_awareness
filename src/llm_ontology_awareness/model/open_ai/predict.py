#!/usr/bin/env python

from dotenv import load_dotenv
from llm_ontology_awareness.model.open_ai.datasets.term_typing import (
    TermTypingRankedRetrievalDataset,
)
from openai import OpenAI

load_dotenv()


def predict(dataset, run_args):

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    pass


if __name__ == "__main__":
    import argparse
