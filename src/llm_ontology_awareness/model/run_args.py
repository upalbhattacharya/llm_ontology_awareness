#!/usr/bin/env python
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RunArguments:
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
    device_map: Optional[int] = field(
        default=0, metadata={"help": "GPU to load model on"}
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
    ontology_task_name: Optional[str] = field(
        default="individual_to_class",
        metadata={"help": "Name to Ontology Awareness task"},
    )
    prompt_strategy_name: Optional[str] = field(
        default="zero-shot", metadata={"help": "Prompting strategy"}
    )
