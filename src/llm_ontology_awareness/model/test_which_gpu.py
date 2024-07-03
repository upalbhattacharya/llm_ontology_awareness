#!/usr/bin/env python

import torch
import logging

logging.info(f"Is GPU available? {torch.cuda.is_available()}")
if torch.cuda.is_available():
    logging.info(f"CUDA device ID: {torch.cuda.current_device()}")
