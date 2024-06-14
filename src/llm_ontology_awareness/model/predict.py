#!/usr/bin/env python

from typing import Iterable

from transformers import AutoTokenizer

from llm_ontology_awareness.model.dataset import IndividualToClassInstructBinaryDataset
from llm_ontology_awareness.model.initialize_model import initialize_model
from llm_ontology_awareness.model.run_args import RunArguments


def predict(model, tokenizer, dataset, **kwargs):
    results = []
    for i, (prompt, label) in enumerate(iter(dataset)):
        tokenized = tokenizer(prompt, return_tensors="pt")
        result = model.generate(tokenized.input_ids, max_new_tokens=3)
        result = tokenizer.batch_decode(result)[0]
        results.append(result.replace(f"{prompt}", ""))

        if kwargs["stop"] and i == kwargs["stop"]:
            break

    return results


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    in_file = "data.json"
    model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, token=os.environ.get("HF_TOKEN")
    )
    dataset = IndividualToClassInstructBinaryDataset(in_file, model_name)
    run_args = RunArguments()
    model = initialize_model(run_args)
    results = predict(model, tokenizer, dataset, stop=19)
    with open("results.txt", "w") as f:
        f.writelines(results)
