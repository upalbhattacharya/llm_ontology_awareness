#!/usr/bin/env python

import logging
import logging.config

LOG_CONF = {
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(name)s %(module)s:%(funcName)s %(lineno)d:: %(message)s"
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "verbose",
        },
        "file_handler": {
            "class": "llm_ontology_awareness.model.utilities.handlers.RollingFileHandler",
            "formatter": "verbose",
            "filename": "run.log",
            # ".": {"suffix": "%Y-%m-%d.log"},
            # "when": "S",
            # "interval": 1,
            "mode": "a",
            "backupCount": 2,
            "maxBytes": 1024,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "": {"handlers": ["stdout", "file_handler"]},
    },
}

logging.config.dictConfig(LOG_CONF)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    print(logger.name)  # root
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
