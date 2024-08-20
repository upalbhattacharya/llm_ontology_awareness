#!/usr/bin/env python

import os
from time import strftime
from typing import Optional

from dataclasses_json import dataclass_json
from pydantic import BaseModel, Field
from transformers import TrainingArguments

ontology_probe_types = ["individual_to_class"]
prompt_strategy_types = ["zero_shot", "few_shot"]
task_types = ["binary_classify", "multi_label_classify"]


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
    load_in_8bit: Optional[bool] = Field(
        default=False, metadata={"help": "Load model with 8-bit precision"}
    )
    load_in_4bit: Optional[bool] = Field(
        default=True, metadata={"help": "Load model with 4-bit precision"}
    )
    device: Optional[int] = Field(default=0, metadata={"help": "GPU to load model on"})
    trust_remote_code: Optional[bool] = Field(
        default=True, metadata={"help": "Enable `trust_remote_code`"}
    )
    training_args: Optional[TrainingArguments] = Field(
        default=None, metadata={"help": "HuggingFace `TrainingArguments` for a Trainer"}
    )
    system_message: Optional[str] = Field(
        default=None, metadata={"help": "System message to use for the model"}
    )
    user_prompt_template: Optional[str] = Field(
        default=None,
        metadata={"help": "User input template to use for text inputs to model"},
    )

    def model_post_init(self, __context):

        # Validation
        if self.load_in_8bit and self.load_in_4bit:
            raise ValueError("Cannot load in 4 bit and 8 bit simultaneously")

        if (
            self.ontology_probe_type is not None
            and self.ontology_probe_type not in ontology_probe_types
        ):
            raise ValueError(
                f"`ontology_probe_type` must be one of {ontology_probe_types}"
            )

        if (
            self.prompt_strategy_type is not None
            and self.prompt_strategy_type not in prompt_strategy_types
        ):
            raise ValueError(
                f"`prompt_strategy_type` must be one of {prompt_strategy_types}"
            )

        if self.task_type is not None and self.task_type not in task_types:
            raise ValueError(f"`task_type` must be one of {task_types}")

        # Updation
        self.output_dir = "output" if self.output_dir is None else self.output_dir
        timestamp = strftime("%Y-%m-%d-%H-%M-%S")
        self.output_dir = os.path.join(self.output_dir, timestamp)

        if self.training_args is not None:
            self.training_args.output_dir = self.output_dir
            self.training_args.logging_dir = self.output_dir


if __name__ == "__main__":
    import json

    from pydantic_core import from_json
    from transformers import TrainingArguments

    # Quick Test
    with open("../../../../run_args/run_args_test.json", "r") as f:
        raw = f.read()
        run_args = RunArguments.parse_raw(raw)
    print(run_args)
    print(run_args.dict())
    with open("test.json", "w") as f:
        # args_save = run_args.to_dict()
        model_dump = run_args.model_dump()
        json.dump(model_dump, f, indent=4)
