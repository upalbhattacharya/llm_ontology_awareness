#!/usr/bin/env python
import os
import time
from logging import FileHandler
from time import strftime


class DateFileHandler(FileHandler):

    def __init__(
        self, filename, mode="a", maxBytes=0, backupCount=0, encoding=None, delay=False
    ):
        self.last_backup_cnt = 0
        new_filename = os.path.join(
            os.path.dirname(filename),
            strftime("%Y-%m-%d") + f"_{os.path.basename(filename)}",
        )
        super(RollingFileHandler, self).__init__(
            filename=new_filename,
            mode=mode,
            maxBytes=maxBytes,
            backupCount=backupCount,
            encoding=encoding,
            delay=delay,
        )

    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        self.last_backup_cnt += 1
        nextName = "%s.%d" % (self.baseFilename, self.last_backup_cnt)
        # if self.backupCount > 0:
        #     for i in range(self.backupCount - 1, 0, -1):
        #         sfn = self.rotation_filename("%s.%d" % (self.baseFilename, i))
        #         dfn = self.rotation_filename("%s.%d" % (self.baseFilename, i + 1))
        #         if os.path.exists(sfn):
        #             if os.path.exists(dfn):
        #                 os.remove(dfn)
        #             os.rename(sfn, dfn)
        #     dfn = self.rotation_filename(self.baseFilename + ".1")
        #     if os.path.exists(dfn):
        #         os.remove(dfn)
        self.rotate(self.baseFilename, nextName)
        if not self.delay:
            self.stream = self._open()
