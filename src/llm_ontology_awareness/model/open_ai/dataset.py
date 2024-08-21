#!/usr/bin/env python

"""
Module to generate different datasets for various prompts for Llama3 models.
"""

import json
from itertools import product

import polars as pl
from torch.utils.data import Dataset


class ClassAssertionOpenAIDataset(Dataset):
    """Generate various individual to class mapping prompts"""

    def __init__(
        self,
        in_file: str,
        system_message: str,
        user_prompt_template: str,
    ):
        self.df = pl.read_ndjson(in_file)
        self.system_message: str = system_message
        self.user_prompt_template: str = user_prompt_template

    def __len__(self):
        return self.df.select(pl.len()).item()

    def __getitem__(self, idx):
        *ents, label = self.df.row(idx)
        # TODO: Make format more generalizable
        messages = [
            {
                "role": "system",
                "content": self.system_message,
            },
            {
                "role": "user",
                "content": self.user_prompt_template.format(*ents),
            },
        ]
        return (
            *ents,
            messages,
            label,
        )


if __name__ == "__main__":

    from llm_ontology_awareness.model.hugging_face.run_args import RunArguments

    in_file = "/home/upal/Data/ontologies/wines-ontology/data/individual_to_class/2024-06-13/data.json"

    with open("../../../../run_args/run_args_test.json", "r") as f:
        raw = f.read()
        run_args = RunArguments.parse_raw(raw)
    itcib = ClassAssertionOpenAIDataset(
        in_file,
        system_message=run_args.system_message,
        user_prompt_template=run_args.user_prompt_template,
    )
    print(len(itcib))
    num_samples = len(itcib)
    itcib = iter(itcib)
    for i in range(num_samples):
        print(i)
        inst, cl, template, label = next(itcib)
        print(template)
