#!/usr/bin/env python

import os
from typing import Optional

from dataclasses_json import dataclass_json
from pydantic import BaseModel, Field
from transformers import TrainingArguments


class RunArguments(BaseModel):
    input: Optional[str] = Field(
        default=None, metadata={"help": "Dataset file to load"}
    )
    output_dir: Optional[str] = Field(
        default=None, metadata={"help": "Directory to save run data"}
    )
    ontology_probe_type: Optional[str] = Field(
        default=None,
        metadata={"help": "Name of Ontology Awareness task to probe"},
    )
    prompt_strategy_type: Optional[str] = Field(
        default=None, metadata={"help": "Prompting strategy"}
    )
    task_type: Optional[str] = Field(default=None, metadata={"help": "Type of task"})
    llm_name: Optional[str] = Field(
        default=None,
        metadata={"help": "Name of model to load"},
    )
    max_tokens: Optional[int] = Field(
        default=1, metadata={"help": "Maximum number of tokens to generate"}
    )
    system_message: Optional[str] = Field(
        default=None, metadata={"help": "System message to use for the model"}
    )
    user_prompt_template: Optional[str] = Field(
        default=None,
        metadata={"help": "User input template to use for text inputs to model"},
    )
    description: Optional[str] = Field(
        default=None,
        metadata={"help": "Description of the task"},
    )
    kwargs: Optional[dict] = Field(
        default={},
        metadata={
            "help": "Named extra arguments. (Used for different types of prompts)"
        },
    )

    def model_post_init(self, __context):

        self.output_dir = "output" if self.output_dir is None else self.output_dir


if __name__ == "__main__":
    import json

    from pydantic_core import from_json
    from transformers import TrainingArguments

    # Quick Test
    with open(
        "/home/upal/Repos/llm_ontology_awareness/run_args/individual_to_class/ranked-retrieval/run_args_ranked_retrieval_test.json",
        "r",
    ) as f:
        raw = f.read()
        print(raw)
        run_args = RunArguments.parse_raw(raw)
    print(run_args)
    print(run_args.dict())
    with open("test.json", "w") as f:
        # args_save = run_args.to_dict()
        model_dump = run_args.model_dump()
        json.dump(model_dump, f, indent=4)
