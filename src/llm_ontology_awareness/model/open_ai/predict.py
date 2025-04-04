#!/usr/bin/env python
"""Prediction script for non-Batch API models"""

import logging
from typing import Dict, Tuple

import polars as pl
from dotenv import load_dotenv
from llm_ontology_awareness.model.open_ai.datasets.term_typing import (
    TermTypingRankedRetrievalDataset,
)
from openai import OpenAI
from tqdm import tqdm

load_dotenv()


def predict(test_data, run_args, **kwargs) -> Tuple[pl.DataFrame, pl.DataFrame]:

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    responses = []
    label_mapping = []
    num_samples = len(test_data)
    test_data = iter(test_data)
    for i in tqdm(range(num_samples)):
        inst, prompt, label = next(test_data)
        # TODO: Quickfix. Change later
        if run_args.llm_name == "o1-preview":
            system_message = prompt.pop(0)
            prompt[0]["content"] = (
                system_message["content"] + "\n" + prompt[0]["content"]
            )
        label_mapping.append((f"task-{i}", inst, label))

        if run_args.llm_name == "o1-preview":
            completion = client.chat.completions.create(
                model=run_args.llm_name,
                messages=prompt,
            )
        else:
            completion = client.chat.completions.create(
                model=run_args.llm_name,
                max_completion_tokens=run_args.max_tokens,
                messages=prompt,
            )

        response = completion.choices[0].message.content
        responses.append((f"task-{i}", response))
        # Quick stop for prototyping
        if kwargs.get("stop", -1) == i:
            break

    label_mapping_df = pl.DataFrame(
        label_mapping,
        schema=[
            ("Custom ID", str),
            ("Individual", str),
            ("Member", list[str]),
        ],
    )

    df = pl.DataFrame(
        responses,
        schema=[
            ("Custom ID", str),
            ("Response", str),
        ],
    )

    return label_mapping_df, df


if __name__ == "__main__":
    import argparse
    import json
    import logging.config
    import os

    from llm_ontology_awareness.model.common.utilities.logging_conf import LOG_CONF
    from llm_ontology_awareness.model.hugging_face.run_args import RunArguments

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

    dir_name = os.path.splitext(os.path.basename(args.args_file))[0]
    output_dir = os.path.join(run_args.output_dir, dir_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    count = len(os.listdir(output_dir)) + 1
    runs_dir = os.path.join(output_dir, "runs", f"run_{count}")
    if not os.path.exists(runs_dir):
        os.makedirs(runs_dir)

    config = LOG_CONF
    config["handlers"]["file_handler"]["dir"] = runs_dir

    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)

    test_data = TermTypingRankedRetrievalDataset(
        run_args.input,
        system_message=run_args.system_message,
        user_prompt_template=run_args.user_prompt_template,
        task_type=run_args.task_type,
        **run_args.kwargs,
    )

    with open(os.path.join(output_dir, "params.json"), "w") as f:
        params_dump = run_args.model_dump()
        json.dump(params_dump, f, indent=4)

    label_mapping_df, df = predict(test_data, run_args)
    label_mapping_df.write_ndjson(os.path.join(runs_dir, "label_mapping.json"))
    df.write_ndjson(os.path.join(runs_dir, "responses.json"))
