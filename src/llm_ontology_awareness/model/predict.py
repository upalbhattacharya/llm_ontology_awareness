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
    responses = []
    y_true = []
    for i, (inst, cl, prompt, label) in enumerate(iter(dataset)):
        y_true.append(label)
        tokenized = tokenizer(prompt, return_tensors="pt").to("cuda")
        response = model.generate(tokenized.input_ids, max_new_tokens=3).cpu()
        response = tokenizer.batch_decode(response)[0]
        responses.append((inst, cl, response.replace(prompt, "")))

        if kwargs.get("stop", None) is not None and i == kwargs["stop"]:
            break

    df = pl.DataFrame(
        responses, schema=[("Individual", str), ("Class", str), ("Response", str)]
    )

    df = df.with_columns(
        pl.col("Response")
        .map_elements(
            function=format_types[run_args.task_type]["function"],
            return_dtype=format_types[run_args.task_type]["return_dtype"],
        )
        .alias("Prediction")
    )
    metrics = task_metrics[run_args.task_type](y_true, df.get_column("Prediction"))

    return df, metrics


if __name__ == "__main__":
    import argparse
    import json
    import logging.config
    import os

    from dotenv import load_dotenv

    from llm_ontology_awareness.model.utilities.logging_conf import LOG_CONF

    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--args_file",
        help="Path to `RunArguments` file",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    with open(args.args_file, "r") as f:
        args_raw = f.read()
        run_args = RunArguments.parse_raw(args_raw)
    config = LOG_CONF
    config["handlers"]["file_handler"]["dir"] = run_args.output_dir
    if not os.path.exists(run_args.output_dir):
        os.makedirs(run_args.output_dir)

    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    logger.info("Test running")
    tokenizer = AutoTokenizer.from_pretrained(
        run_args.llm_name, token=os.environ.get("HF_TOKEN")
    )
    dataset = IndividualToClassNoStructureDirectMembershipInstructBinaryDataset(
        run_args.input, run_args.llm_name
    )
    model = initialize_model(run_args)
    with open(args.output_dir / "params.json", "w") as f:
        params_dump = run_args.model_dump()
        json.dump(params_dump, f, indent=4)

    df, metrics = predict(model, tokenizer, dataset, run_args, stop=19)
    df.write_ndjson(run_args.output_dir / "responses.json")
    with open(run_args.output_dir / "pred_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
