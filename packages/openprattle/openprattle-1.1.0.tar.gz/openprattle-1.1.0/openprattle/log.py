"""Setup logging for oprattle."""

import warnings
import logging.handlers
import sys
import textwrap
from subprocess import CalledProcessError

LOGGING_HANDLER = None

def init_logger(json = False):
    """
    Init the package wide logger.
    
    :param json: If True, logging output will be wrapped in JSON to allow for easier parsing by other programs.
    """
    global LOGGING_HANDLER
    
    logging.captureWarnings(True)
    
    logger = logging.getLogger("openprattle")
    warnings_logger = logging.getLogger("py.warnings")
    
    # Choose our handler.
    LOGGING_HANDLER = logging.StreamHandler(sys.stderr)
        
    # Handle everything.
    LOGGING_HANDLER.setLevel(logging.DEBUG)

    # Set its formatter, depending on what we've been asked to do.
    if not json:
        formatter = logging.Formatter()
    
    else:
        formatter = JSON_formatter()

    LOGGING_HANDLER.setFormatter(formatter)
    
    # Remove old handlers.
    loggers = (logger, warnings_logger)
    for log in loggers:
        while len(log.handlers) > 0:
            log.removeHandler(log.handlers[0])
            
        log.addHandler(LOGGING_HANDLER)
    
    
class JSON_formatter(logging.Formatter):
    """
    A logging formatter that prints JSON.
    """

    def format(self, record):
        import json
        return json.dumps({
            'logger': record.name,
            'levelno': record.levelno,
            'message': record.getMessage(),
            'exception': self.formatException(record.exc_info) if record.exc_info else ""
        })
    
init_logger()