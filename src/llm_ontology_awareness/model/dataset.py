#!/usr/bin/env python

"""
Module to generate different datasets for various prompts for Llama3 models.
"""

import json
from itertools import product

import polars as pl
from torch.utils.data import Dataset

with open("settings/model_templates.json", "r") as f:
    model_templates = json.load(f)


class IndividualToClassInstructBinaryDataset(Dataset):
    """Generate various individual to class mapping prompts"""

    def __init__(self, in_file: str, model_name: str):
        self.df = pl.read_ndjson(in_file)
        self.prompt_template: str = model_templates[model_name]
        self.system_message: str = (
            "You are a helpful assistant that classifies statements as True or False"
        )
        self.classify_statement: str = "{} is a {}"

    def __len__(self):
        return self.df["Individual"].unique().len() * self.df["Class"].unique().len()

    def __getitem__(self, idx):
        inst, cl, label = self.df.row(idx)
        sentence = self.classify_statement.format(inst, cl)
        return self.prompt_template.format(self.system_message, sentence), label


if __name__ == "__main__":
    print("Running")
    in_file = "/home/upal/Data/ontologies/wines-ontology/data/individual_to_class/2024-06-13/data.json"
    itcib = IndividualToClassInstructBinaryDataset(
        in_file, "meta-llama/Meta-Llama-3-8B-Instruct"
    )
    for i, (d, label) in enumerate(iter(itcib)):
        print(d, label)
        if i == 19:
            break
