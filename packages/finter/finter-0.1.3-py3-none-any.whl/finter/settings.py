import logging
import traceback

import finter
from dotenv import load_dotenv

load_dotenv()


def check_configuration():
    configuration = finter.Configuration()
    if configuration.api_key["Authorization"] == "Token None":
        error_message = (
            "API Key is not set. Please set the API Key to proceed.\n\n"
            "You can set the API Key in one of the following ways:\n"
            "- By setting an environment variable directly in your environment:\n"
            "    import os\n"
            "    os.environ['FINTER_API_KEY'] = 'YOUR_API_KEY'\n\n"
            "- By adding the following line to a .env file located in the project root:\n"
            "    FINTER_API_KEY='YOUR_API_KEY'"
        )
        raise ValueError(error_message)
    return configuration


def get_api_client():
    return finter.ApiClient(check_configuration())


def log_section(title):
    original_formatter = log_handler.formatter

    log_handler.setFormatter(logging.Formatter("%(message)s"))

    separator = "=" * 40
    header = f"\n{separator} {title} {separator}"
    logger.info(header)

    log_handler.setFormatter(original_formatter)


def log_with_traceback(message):
    logger.error(message)
    logger.error(traceback.format_exc())


logger = logging.getLogger("finter_sdk")
logger.setLevel(logging.INFO)

log_handler = logging.StreamHandler()
log_handler.setLevel(logging.INFO)  # 필요한 로깅 레벨 설정
logger.addHandler(log_handler)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_handler.setFormatter(formatter)
