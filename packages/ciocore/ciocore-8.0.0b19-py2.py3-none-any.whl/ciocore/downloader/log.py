import logging
 
LOGGER_NAME = "conductor.download"

FORMATTER = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)8s %(filename)s:%(lineno)d %(threadName)s> %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
    "NOTSET": logging.NOTSET,
}


class GracefulStreamHandler(logging.StreamHandler):
    """
    A custom StreamHandler that suppresses BrokenPipeError.
    
    This handler extends the standard logging.StreamHandler to gracefully handle 
    BrokenPipeErrors that can occur when output streams are closed prematurely. 
    It overrides the emit method to catch and ignore BrokenPipeError, allowing 
    the program to continue without interruption.
    """
    
    def emit(self, record):
        """
        Overrides the StreamHandler.emit method to gracefully handle BrokenPipeError.

        Args:
            record (logging.LogRecord): The log record to be emitted.
        """
        try:
            super().emit(record)
        except BrokenPipeError:
            pass

# Create a logger and add a custom StreamHandler
logger = logging.getLogger(LOGGER_NAME)
stream_handler = GracefulStreamHandler()
stream_handler.setFormatter(FORMATTER)
logger.addHandler(stream_handler)

