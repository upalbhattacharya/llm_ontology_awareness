#!/usr/bin/env python

"""
Module to generate different datasets for various prompts for Llama3 models.
"""

import polars as pl
from torch.utils.data import Dataset

from llm_ontology_awareness.task_map.term_typing import task_types


class TermTypingHFDataset(Dataset):
    """Generate various individual to class mapping prompts"""

    def __init__(
        self,
        in_file: str,
        model_name: str,
        system_message: str,
        user_prompt_template: str,
    ):
        self.df = pl.read_ndjson(in_file)
        self.prompt_template: str = system_message_templates[model_name]
        self.system_message: str = system_message
        self.user_prompt_template: str = user_prompt_template

    def __len__(self):
        return self.df.select(pl.len()).item()

    def __getitem__(self, idx):
        *ents, label = self.df.row(idx)
        sentence = self.user_prompt_template.format(*ents)
        return (
            *ents,
            self.prompt_template.format(self.system_message, sentence),
            label,
        )


class TermTypingRankedRetrievalDataset(Dataset):
    """Generate Ranked retrieval prompts for class assertions"""

    def __init__(
        self,
        in_file: str,
        system_message: str,
        user_prompt_template: str,
        task_type: str,
        **kwargs,
    ):
        self.task_type = task_type
        if self.task_type not in list(task_types.keys()):
            raise KeyError(
                f"`task_type` must be one of: {list(task_types.keys())}. Got {self.task_type}"
            )
        self.df = pl.read_ndjson(in_file)
        self.system_message: str = system_message
        self.user_prompt_template: str = user_prompt_template
        self.extra_args = kwargs
        self.classes = list(
            set([cls for items in self.df["Ranked List"].to_list() for cls in items])
        )
        if not self.extra_args:
            self.extra_args = {}

    def __len__(self):
        return self.df.select(pl.len()).item()

    def __getitem__(self, idx):
        *ents, label = self.df.row(idx)
        messages = [
            {
                "role": "system",
                "content": self.system_message.format(
                    **self.extra_args, classes=self.classes
                ),
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
    itcib = TermTypingHFDataset(
        in_file,
        model_name=run_args.llm_name,
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
