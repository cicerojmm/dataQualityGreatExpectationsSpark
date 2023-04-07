import logging
from logging.config import dictConfig


def get_logger():
    logging_config = {
        'version': 1,
        'formatters': {
            'f': {
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
            }
        },
        'handlers': {
            'h': {
                'class': 'logging.StreamHandler',
                'formatter': 'f',
                'level': 20
            }
        },
        'root': {
            'handlers': [
                'h'
            ],
            'level': 10
        }
    }

    dictConfig(logging_config)

    logger = logging.getLogger()
    return logger
