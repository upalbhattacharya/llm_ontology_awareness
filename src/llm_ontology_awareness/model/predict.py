#!/usr/bin/env python

import polars as pl
from transformers import AutoTokenizer

from llm_ontology_awareness.model.dataset import (
    IndividualToClassNoStructureDirectMembershipInstructBinaryDataset,
)
from llm_ontology_awareness.model.format_response import format_types
from llm_ontology_awareness.model.initialize_model import initialize_model
from llm_ontology_awareness.model.metrics import task_metrics
from llm_ontology_awareness.model.run_args import RunArguments


def predict(model, tokenizer, dataset, run_args, **kwargs) -> (pl.DataFrame, dict):
    y_pred = []
    y_true = []
    for i, (inst, cl, prompt, label) in enumerate(iter(dataset)):
        y_true.append(label)
        tokenized = tokenizer(prompt, return_tensors="pt").to("cuda")
        pred = model.generate(tokenized.input_ids, max_new_tokens=3).cpu()
        pred = tokenizer.batch_decode(pred)[0]
        y_pred.append((inst, cl, pred.replace(prompt, "")))

        if kwargs["stop"] and i == kwargs["stop"]:
            break

    df = pl.DataFrame(
        y_pred, schema=[("Individual", str), ("Class", str), ("Response", str)]
    )

    df = df.with_columns(
        pl.col("Response")
        .map_elements(
            function=format_types[run_args.task_name]["function"],
            return_dtype=format_types[run_args.task_name]["return_dtype"],
        )
        .alias("Prediction")
    )
    metrics = task_metrics[run_args.task_name](y_true, y_pred)

    return df, metrics


if __name__ == "__main__":
    import argparse
    import json
    import os
    from pathlib import Path

    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", help="Path to dataset file to read", type=str, required=True
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="Path to save generated outputs",
        type=str,
        default=None,
    )
    args = parser.parse_args()
    if args.output_dir is None:
        args.output_dir = Path(args.file).parents[0]

    model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, token=os.environ.get("HF_TOKEN")
    )
    dataset = IndividualToClassNoStructureDirectMembershipInstructBinaryDataset(
        args.file, model_name
    )
    run_args = RunArguments()
    model = initialize_model(run_args)
    df, metrics = predict(model, tokenizer, dataset, run_args, stop=19)
    df.write_ndjson(args.output_dir / "responses.json")
    with open(args.output_dir / "pred_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
