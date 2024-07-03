#!/usr/bin/env python

import logging

import torch


def get_device_info():
    logging.info(f"Is CUDA available? {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        logging.info(f"No. of CUDA device(s): {torch.cuda.device_count()}")
        logging.info(f"CUDA Device ID: {torch.cuda.current_device()}")
