#!/usr/bin/env python
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ScriptArguments:
    model_name: Optional[str] = field(
        default="meta-llama/Meta-Llama-3-8B-Instruct",
        metadata={"help": "Name of model to load"},
    )
    load_in_8bit: Optional[bool] = field(
        default=False, metadata={"help": "Load model with 8-bit precision"}
    )
    load_in_4bit: Optional[bool] = field(
        default=True, metadata={"help": "Load model with 4-bit precision"}
    )
    input_file: Optional[str] = field(
        default="data_pl.json", metadata={"help": "Dataset file to load"}
    )
    output_dir: Optional[str] = field(
        default="output", metadata={"help": "Directory to save output to"}
    )
    trust_remote_code: Optional[bool] = field(
        default=True, metadata={"help": "Enable `trust_remote_code`"}
    )
