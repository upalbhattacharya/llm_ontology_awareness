#!/usr/bin/env python

import os
from dataclasses import dataclass, field
from time import strftime
from typing import Optional

from dataclasses_json import dataclass_json

ontology_probe_types = ["individual_to_class"]
prompt_strategy_types = ["zero_shot", "few_shot"]
task_types = ["binary_classify", "multi_label_classify"]


@dataclass_json
@dataclass
class RunArguments:
    input: Optional[os.PathLike] = field(
        default=None, metadata={"help": "Dataset file to load"}
    )
    output_dir: Optional[os.PathLike] = field(
        default=None, metadata={"help": "Directory to save run data"}
    )
    ontology_probe_type: Optional[str] = field(
        default=None,
        metadata={"help": "Name of Ontology Awareness task to probe"},
    )
    prompt_strategy_type: Optional[str] = field(
        default=None, metadata={"help": "Prompting strategy"}
    )
    task_type: Optional[str] = field(default=None, metadata={"help": "Type of task"})
    model_name: Optional[str] = field(
        default=None,
        metadata={"help": "Name of model to load"},
    )
    load_in_8bit: Optional[bool] = field(
        default=False, metadata={"help": "Load model with 8-bit precision"}
    )
    load_in_4bit: Optional[bool] = field(
        default=True, metadata={"help": "Load model with 4-bit precision"}
    )
    device_map: Optional[int] = field(
        default=0, metadata={"help": "GPU to load model on"}
    )
    trust_remote_code: Optional[bool] = field(
        default=True, metadata={"help": "Enable `trust_remote_code`"}
    )

    def __post_init__(self):

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


if __name__ == "__main__":
    import json

    # Quick Test
    with open("../../../runs/run_args_1.json", "r") as f:
        args = json.load(f)
        print(args)
        run_args = RunArguments().from_dict(args)
    print(run_args)
    with open("test.json", "w") as f:
        args_save = run_args.to_dict()
        json.dump(args_save, f, indent=4)
