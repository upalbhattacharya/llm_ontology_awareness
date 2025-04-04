#!/usr/bin/env python

"""
Module to generate different datasets for various prompts for Llama3 models.
"""

from typing import Optional

import polars as pl
from llm_ontology_awareness.task_map.term_typing import task_types
from torch.utils.data import Dataset


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
        examples_file: Optional[str] = None,
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
            messages = [
                {
                    "role": "system",
                    "content": self.system_message.format(
                        **self.extra_args,
                        classes=self.classes,
                        examples=self.generate_examples(),
                    ),
                },
                {"role": "user", "content": self.user_prompt_template.format(*ents)},
            ]
        else:
           
                

#         if self.examples is not None:
#             messages = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

# {self.system_message.format(**self.extra_args, classes=self.classes, examples=self.generate_examples())}<|eot_id|><|start_header_id|>user<|end_header_id|>

# {self.user_prompt_template.format(*ents)}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
#         else:
#             messages = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

# {self.system_message.format(**self.extra_args, classes=self.classes)}<|eot_id|><|start_header_id|>user<|end_header_id|>

# {self.user_prompt_template.format(*ents)}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

        return (
            *ents,
            messages,
            label,
        )


if __name__ == "__main__":
    import argparse

    from llm_ontology_awareness.model.hugging_face.run_args import RunArguments

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--data", help="Path to data DataFrame", type=str, required=True
    )
    parser.add_argument(
        "-r", "--run_args", help="Path to RunArguments", type=str, required=True
    )

    args = parser.parse_args()

    with open(args.run_args, "r") as f:
        raw = f.read()
        run_args = RunArguments.parse_raw(raw)

    itcib = TermTypingRankedRetrievalDataset(
        args.data,
        system_message=run_args.system_message,
        user_prompt_template=run_args.user_prompt_template,
        task_type=run_args.task_type,
        examples_file=run_args.examples_file,
        **run_args.kwargs,
    )
    print(len(itcib))
    num_samples = len(itcib)
    itcib = iter(itcib)
    for i in range(num_samples):
        print(i)
        inst, template, label = next(itcib)
        print(template)
