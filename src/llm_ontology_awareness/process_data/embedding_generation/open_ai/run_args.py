#!/usr/bin/env python

from typing import Optional

from pydantic import BaseModel, Field


class RunArguments(BaseModel):
    input: Optional[str] = Field(
        default=None, metadata={"help": "Dataset file to load"}
    )
    output_dir: Optional[str] = Field(
        default=None, metadata={"help": "Directory to save run data"}
    )
    model: Optional[str] = Field(
        default="text-embedding-3-large", metadata={"help": "Embedding model to use"}
    )
    dimensions: Optional[int] = Field(
        default=1024, metadata={"help": "Embedding dimension"}
    )
    encoding_format: Optional[str] = Field(
        default="float", metadata={"help": "Format to return data"}
        
    def model_post_init(self, __context):

        self.output_dir = "output" if self.output_dir is None else self.output_dir
