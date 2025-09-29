import logging
import sys


def setup_logger():
    log = logging.getLogger('nopcommerce_framework')
    log.setLevel(logging.INFO)

    if not log.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        log.addHandler(handler)

    return log


logger = setup_logger()
