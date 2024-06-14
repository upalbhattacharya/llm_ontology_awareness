#!/usr/bin/env python

import os

import torch
import torch.nn as nn
from dotenv import load_dotenv
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    PretrainedConfig,
)

from llm_ontology_awareness.modelling.models.llama3.params import ScriptArguments

load_dotenv()


def initialize_model(script_args: ScriptArguments):
    if script_args.load_in_8bit and script_args.load_in_4bit:
        raise ValueError(
            "You can't load the model in 8 bits and 4 bits at the same time"
        )
    elif script_args.load_in_8bit or script_args.load_in_4bit:
        quantization_config = BitsAndBytesConfig(
            load_in_8bit=script_args.load_in_8bit,
            load_in_4bit=script_args.load_in_4bit,
        )
        device_map = {"": 0}
        torch_dtype = torch.bfloat16
    else:
        device_map = None
        quantization_config = None
        torch_dtype = None
    model = AutoModelForCausalLM.from_pretrained(
        script_args.model_name,
        quantization_config=quantization_config,
        device_map=device_map,
        trust_remote_code=script_args.trust_remote_code,
        torch_dtype=torch_dtype,
        token=os.environ.get("HF_TOKEN"),
    )
    return model
