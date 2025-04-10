#!/usr/bin/env python

import polars as pl
from llm_ontology_awareness.model.hugging_face.datasets.term_typing import (
    TermTypingRankedRetrievalDataset,
)
from llm_ontology_awareness.model.hugging_face.initialize_model import initialize_model
from llm_ontology_awareness.model.hugging_face.run_args import RunArguments
from tqdm import tqdm
from transformers import AutoTokenizer


def predict(model, tokenizer, test_data, run_args, **kwargs) -> pl.DataFrame:
    responses = []
    label_mapping = []
    num_samples = len(test_data)
    test_data = iter(test_data)
    tokenizer.pad_token = tokenizer.eos_token
    for i in tqdm(range(num_samples)):
        inst, messages, label = next(test_data)
        label_mapping.append((f"task-{i}", inst, label))
        input_ids = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            padding=True,
            return_tensors="pt",
        ).to(f"cuda:{run_args.device}")
        prompt = tokenizer.decode(input_ids[0])
        print(prompt)
        gen_tokens = model.generate(
            input_ids,
            max_new_tokens=run_args.max_tokens,
            temperature=run_args.temperature,
        ).cpu()
        response = tokenizer.batch_decode(
            gen_tokens[:, input_ids.shape[1] :], skip_special_tokens=True
        )[0]
        print(response)
        responses.append((f"task-{i}", response))

        if kwargs.get("stop", None) is not None and i == kwargs["stop"]:
            break

    label_mapping_df = pl.DataFrame(
        label_mapping,
        schema=[
            ("Custom ID", str),
            ("Individual", str),
            ("Member", list[str]),
        ],
    )

    df = pl.DataFrame(responses, schema=[("Custom ID", str), ("Response", str)])

    # df = df.with_columns(
    #     pl.col("Response")
    #     .map_elements(
    #         function=format_types[run_args.task_type]["function"],
    #         return_dtype=format_types[run_args.task_type]["return_dtype"],
    #     )
    #     .alias("Prediction")
    # )

    return label_mapping_df, df


if __name__ == "__main__":
    import argparse
    import json
    import logging.config
    import os

    import torch
    from dotenv import load_dotenv
    from llm_ontology_awareness.model.common.utilities.logging_conf import LOG_CONF
    from llm_ontology_awareness.model.common.utilities.utils import get_device_info

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

    # Add run information
    if not os.path.exists(output_dir):
        output_dir = os.path.join(output_dir, "run_1")
    else:
        run_num = len(os.listdir(output_dir)) + 1
        output_dir = os.path.join(output_dir, f"run_{run_num}")
    os.makedirs(output_dir)
    torch.set_default_device(f"cuda:{run_args.device}")
    get_device_info()

    config = LOG_CONF
    config["handlers"]["file_handler"]["dir"] = output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    tokenizer = AutoTokenizer.from_pretrained(
        run_args.llm_name, token=os.environ.get("HF_TOKEN")
    )
    test_data = TermTypingRankedRetrievalDataset(
        run_args.input,
        system_message=run_args.system_message,
        user_prompt_template=run_args.user_prompt_template,
        task_type=run_args.task_type,
        examples_file=run_args.examples_file,
        **run_args.kwargs,
    )
    model = initialize_model(run_args)
    with open(os.path.join(output_dir, "params.json"), "w") as f:
        params_dump = run_args.model_dump()
        json.dump(params_dump, f, indent=4)

    label_mapping_df, df = predict(model, tokenizer, test_data, run_args)
    label_mapping_df.write_ndjson(os.path.join(output_dir, "label_mapping.json"))
    df.write_ndjson(os.path.join(output_dir, "responses.json"))
