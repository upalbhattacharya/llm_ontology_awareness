#!/usr/bin/env python

"""
Module to generate different datasets for various prompts for Llama3 models.
"""

from typing import Optional

import polars as pl
from llm_ontology_awareness.task_map.term_typing import task_types
from torch.utils.data import Dataset


class TermTypingBinaryClassificationDataset(Dataset):
    """Generate binary classification prompts for class assertions"""

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
        if not self.extra_args:
            self.extra_args = {}

    def __len__(self):
        return self.df.select(pl.len()).item()

    def __getitem__(self, idx):
        *ents, label = self.df.row(idx)
        messages = [
            {
                "role": "system",
                "content": self.system_message.format(**self.extra_args),
            },
            {
                "role": "user",
                "content": self.user_prompt_template.format(*ents),
            },
        ]
        print((*ents, messages, label))
        return (
            *ents,
            messages,
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
        examples_file: Optional[str] = None,
        llm_name: Optional[str] = "gpt-4o",
        **kwargs,
    ):
        self.task_type = task_type
        if self.task_type not in list(task_types.keys()):
            raise KeyError(
                f"`task_type` must be one of: {list(task_types.keys())}. Got {self.task_type}"
            )
        self.df = pl.read_ndjson(in_file)
        self.examples = (
            pl.read_ndjson(examples_file) if examples_file is not None else None
        )
        self.system_message: str = system_message
        self.user_prompt_template: str = user_prompt_template
        self.extra_args = kwargs
        self.classes = list(
            set([cls for items in self.df["Ranked List"].to_list() for cls in items])
        )
        if not self.extra_args:
            self.extra_args = {}
        self.llm_name = llm_name

    def __len__(self):
        return self.df.select(pl.len()).item()

    def generate_examples(self):
        example_print = ["---"]
        for row in self.examples.rows():
            example_print.append(row[0])
            example_print.extend([f"{i+1}. {val}" for i, val in enumerate(row[1])])
            example_print.append("\n")
        return "\n".join(example_print)

    def __getitem__(self, idx):
        *ents, label = self.df.row(idx)
        if self.examples is not None:
            if self.llm_name == "o1-preview":
                messages = [
                    {
                        "role": "user",
                        "content": self.system_message.format(
                            **self.extra_args,
                            classes=self.classes,
                            examples=self.generate_examples(),
                        )
                        + "\n"
                        + self.user_prompt_template.format(*ents),
                    },
                ]
            else:
                messages = [
                    {
                        "role": "system",
                        "content": self.system_message.format(
                            **self.extra_args,
                            classes=self.classes,
                            examples=self.generate_examples(),
                        ),
                    },
                    {
                        "role": "user",
                        "content": self.user_prompt_template.format(*ents),
                    },
                ]
        else:
            if self.llm_name == "o1-preview":
                messages = [
                    {
                        "role": "user",
                        "content": self.system_message.format(
                            **self.extra_args,
                            classes=self.classes,
                        )
                        + "\n"
                        + self.user_prompt_template.format(*ents),
                    },
                ]
            else:
                messages = [
                    {
                        "role": "system",
                        "content": self.system_message.format(
                            **self.extra_args,
                            classes=self.classes,
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
    import argparse

    from llm_ontology_awareness.model.open_ai.run_args import RunArguments

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--run_args", help="Path to RunArguments", type=str, required=True
    )

    args = parser.parse_args()

    with open(args.run_args, "r") as f:
        raw = f.read()
        run_args = RunArguments.parse_raw(raw)

    itcib = TermTypingRankedRetrievalDataset(
        in_file=run_args.input,
        system_message=run_args.system_message,
        user_prompt_template=run_args.user_prompt_template,
        task_type=run_args.task_type,
        examples_file=run_args.examples_file,
        llm_name=run_args.llm_name,
        **run_args.kwargs,
    )
    num_samples = len(itcib)
    itcib = iter(itcib)
    for i in range(num_samples):
        print(i)
        inst, template, label = next(itcib)
        for r in template:
            print(r["content"])
