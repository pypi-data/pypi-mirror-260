# datafog-python/src/datafog/__init__.py
import json
import logging

import requests

from .__about__ import __version__
from .pii_tools.PresidioEngine import batch_redact, batch_scan, presidio_batch_init

__all__ = [
    "__version__",
    "PresidioEngine",
]
# Create file handler which logs even debug messages

# Configure basic settings for logging to console
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create and configure logger
logger = logging.getLogger(__name__)

# Create file handler which logs debug messages
fh = logging.FileHandler("datafog_debug.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

# Add the file handler to the logger
logger.addHandler(fh)

# Now you can use logger to log messages
logger.debug("This is a debug message")


class DataFog:
    """DataFog class for scanning and redacting PII from text data"""

    def __init__(self):
        self.version = __version__
        logger.debug(f"DataFog version: {self.version}")
        logger.debug(f"Initializing Presidio Engine")
        self.language = "en"
        logger.debug(f"Language: {self.language}")
        self.threshold = 0.5
        logger.debug(f"Threshold: {self.threshold}")
        self.redaction_string = "REDACTED"
        logger.debug(f"Redaction string: {self.redaction_string}")
        self.analyzer, self.batch_analyzer, self.batch_anonymizer = (
            presidio_batch_init()
        )
        logger.debug(f"Analyzer: {self.analyzer}")
        logger.debug(f"Batch Analyzer: {self.batch_analyzer}")
        logger.debug(f"Batch Anonymizer: {self.batch_anonymizer}")

        self.entities = self.analyzer.get_supported_entities()

        logger.debug(f"Supported entities: {self.entities}")

    def __call__(self, input_source, privacy_operation):
        """Scan or redact PII from input source"""

        # Read the input source
        if isinstance(input_source, str):
            if input_source.startswith(("http://", "https://")):
                logger.debug("Downloading file from URL")
                text = requests.get(input_source).text.splitlines()
            elif input_source.endswith(".csv"):
                logger.debug("Reading CSV from local path")
                text = open(input_source).read().splitlines()
            elif input_source.endswith(".txt"):
                logger.debug("Reading TXT from local path")
                text = open(input_source).read().splitlines()
            elif input_source.endswith(".json"):
                logger.debug("Reading JSON from local path")
                text = json.load(open(input_source))
            else:
                logger.debug("Reading text from string")
                text = [input_source]
        else:
            logger.error("Unsupported input source type")
            raise ValueError("Unsupported input source type")

        text = [str(t) for t in text]

        # Process the input based on privacy operation
        if privacy_operation not in ["scan", "redact"]:
            raise ValueError("Unsupported privacy operation")

        text_dict = {"text": text}

        if privacy_operation == "scan":
            print("Scanning for PII")
            results = batch_scan(text_dict, self.batch_analyzer)
        elif privacy_operation == "redact":
            print("Redacting PII")
            results = batch_redact(
                text_dict,
                batch_scan(text_dict, self.batch_analyzer),
                self.batch_anonymizer,
            )

        return [str(result) for result in results]
