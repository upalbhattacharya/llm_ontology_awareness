#!/usr/bin/env python

import logging
import math
import os

import polars as pl
from tqdm import tqdm

from llm_ontology_awareness.model.open_ai.dataset import ClassAssertionOpenAIDataset
from llm_ontology_awareness.model.open_ai.run_args import RunArguments


def create_batch(test_data, run_args, **kwargs) -> (pl.DataFrame, dict):
    tasks = []
    label_mapping = []
    num_samples = len(test_data)
    test_data = iter(test_data)

    for i in tqdm(range(num_samples)):
        inst, cl, messages, label = next(test_data)
        task = {
            "custom_id": f"task-{i}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": run_args.llm_name,
                "messages": messages,
                "max_tokens": run_args.max_tokens,
            },
        }
        tasks.append(task)
        label_mapping.append((f"task-{i}", inst, cl, label))

        if kwargs.get("stop", None) is not None and i == kwargs["stop"]:
            break

    df = pl.DataFrame(
        label_mapping,
        schema=[
            ("Custom ID", str),
            ("Individual", str),
            ("Class", str),
            ("Member", bool),
        ],
    )

    return tasks, df


if __name__ == "__main__":
    import argparse
    import json
    import logging.config

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

    # Get filename to name output directory
    dir_name = os.path.splitext(os.path.basename(args.args_file))[0]
    output_dir = os.path.join(run_args.output_dir, dir_name)

    config = LOG_CONF
    config["handlers"]["file_handler"]["dir"] = os.path.join(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    test_data = ClassAssertionOpenAIDataset(
        run_args.input,
        system_message=run_args.system_message,
        user_prompt_template=run_args.user_prompt_template,
    )
    with open(os.path.join(output_dir, "params.json"), "w") as f:
        params_dump = run_args.model_dump()
        json.dump(params_dump, f, indent=4)

    tasks, df = create_batch(test_data, run_args)
    df.write_ndjson(os.path.join(output_dir, "label_mapping.json"))
    iterator = iter(tasks)
    for i in range(math.ceil(len(tasks) / 50000)):
        with open(
            os.path.join(output_dir, f"batch_tasks_{i + 1}.jsonl"),
            "w",
        ) as f:
            try:
                for j in range(50000):
                    f.write(json.dumps(next(iterator)) + "\n")
            except StopIteration:
                exit(0)