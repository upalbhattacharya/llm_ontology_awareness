#!/usr/bin/env python
import os
from logging import FileHandler


class DirFileHandler(FileHandler):

    def __init__(
        self, filename, dir, mode="a", encoding=None, delay=False, errors=None
    ):
        new_filename = os.path.join(dir, filename)
        super(DirFileHandler, self).__init__(
            new_filename, mode=mode, encoding=encoding, delay=delay, errors=errors
        )
