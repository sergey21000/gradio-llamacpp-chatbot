import os
import sys

from loguru import logger


class IsolationDefaultHandlerFilter:
    def __init__(self, logger_extras: list[str]):
        self.logger_extras = logger_extras

    def __call__(self, record):
        for logger_extra in self.logger_extras:
            if logger_extra in record['extra']:
                return False
        return True


if 0 in logger._core.handlers:
    if hasattr(logger._core.handlers[0]._filter, 'logger_extras'):
        logger._core.handlers[0]._filter.logger_extras.append('chatbot')
    else:
        logger._core.handlers[0]._filter = IsolationDefaultHandlerFilter(
            logger_extras=['chatbot']
        )

# set log level for chatbot app
log_level = os.getenv('CHATBOT_LOG_LEVEL', 'WARNING')
if log_level:
    logger.add(
        sys.stderr,
        level=log_level,
        filter=lambda record: 'chatbot' in record['extra'],
        colorize=True,
    )
    logger = logger.bind(chatbot=True)
