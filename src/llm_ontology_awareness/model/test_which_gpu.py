#!/usr/bin/env python

import torch

print(f"Is GPU available? {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA device ID: {torch.cuda.current_device()}")
