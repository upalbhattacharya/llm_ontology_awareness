#!/usr/bin/env python

import logging
import logging.config
import sys

LOG_CONF = {
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(name)s %(module)s:%(funcName)s %(lineno)d:: %(message)s",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
            "formatter": "verbose",
        },
        "file_handler": {
            "class": "llm_ontology_awareness.model.common.utilities.handlers.DirFileHandler",
            "level": "DEBUG",
            "formatter": "verbose",
            "filename": "run.log",
            "dir": "",
            "mode": "a",
            "encoding": "utf-8",
        },
    },
    "loggers": {"": {"handlers": ["stdout", "file_handler"], "level": "DEBUG"}},
}


def log_exception(exctype, value, traceback):
    logging.critical("Error Information:", exc_info=(exctype, value, traceback))


sys.excepthook = log_exception


if __name__ == "__main__":
    # Quick Test
    config = LOG_CONF
    config["handlers"]["file_handler"]["dir"] = "."
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    print(logger.name)  # root
    print(logger.handlers)
    print(logger.hasHandlers())
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
