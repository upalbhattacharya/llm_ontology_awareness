#!/usr/bin/env python

import logging
import os

import polars as pl
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

from llm_ontology_awareness.model.common.format_response import format_types
from llm_ontology_awareness.model.common.metrics import task_metrics
from llm_ontology_awareness.model.open_ai.dataset import ClassAssertionOpenAIDataset
from llm_ontology_awareness.model.open_ai.run_args import RunArguments

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def predict(test_data, run_args, **kwargs) -> (pl.DataFrame, dict):
    responses = []
    y_true = []
    num_samples = len(test_data)
    test_data = iter(test_data)
    for i in tqdm(range(num_samples)):
        inst, cl, messages, label = next(test_data)

        completion = client.chat.completions.create(
            model=run_args.llm_name, messages=messages, max_tokens=run_args.max_tokens
        )
        y_true.append(label)
        responses.append((inst, cl, completion.choices[0].message.content))

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

    from llm_ontology_awareness.model.common.utilities.logging_conf import LOG_CONF

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
    test_data = ClassAssertionOpenAIDataset(
        run_args.input,
        system_message=run_args.system_message,
        user_prompt_template=run_args.user_prompt_template,
    )
    with open(os.path.join(run_args.output_dir, "params.json"), "w") as f:
        params_dump = run_args.model_dump()
        json.dump(params_dump, f, indent=4)

    df, metrics = predict(test_data, run_args)
    df.write_ndjson(os.path.join(run_args.output_dir, "responses.json"))
    with open(os.path.join(run_args.output_dir, "pred_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)
