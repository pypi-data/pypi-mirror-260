import logging
import colorlog

# Create a logger
logger = logging.getLogger(__name__)

# Create a color formatter
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s%(reset)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white'
    }
)

# Create a console handler and attach the formatter
ch = logging.StreamHandler()
ch.setFormatter(formatter)

# Attach the handler to the logger
logger.addHandler(ch)

# Set the logging level
logger.setLevel(logging.DEBUG)