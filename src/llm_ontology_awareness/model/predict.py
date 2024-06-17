#!/usr/bin/env python

from typing import Iterable

from transformers import AutoTokenizer

from llm_ontology_awareness.model.dataset import IndividualToClassInstructBinaryDataset
from llm_ontology_awareness.model.initialize_model import initialize_model
from llm_ontology_awareness.model.run_args import RunArguments


def predict(model, tokenizer, dataset, **kwargs):
    results = []
    for i, (prompt, label) in enumerate(iter(dataset)):
        tokenized = tokenizer(prompt, return_tensors="pt").to("cuda")
        result = model.generate(tokenized.input_ids, max_new_tokens=3)
        result = tokenizer.batch_decode(result)[0]
        results.append(result.replace(f"{prompt}", ""))

        if kwargs["stop"] and i == kwargs["stop"]:
            break

    return results


if __name__ == "__main__":
    import argparse
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
    if args.output_dir:
        args.output_dir = Path(args.file).parents[0]

    model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, token=os.environ.get("HF_TOKEN")
    )
    dataset = IndividualToClassInstructBinaryDataset(args.file, model_name)
    run_args = RunArguments()
    model = initialize_model(run_args)
    results = predict(model, tokenizer, dataset, stop=19)
    with open(args.output_dir / "results.txt", "w") as f:
        f.writelines(results)
