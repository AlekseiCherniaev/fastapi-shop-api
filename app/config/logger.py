import logging
import logging.config


def setup_logger(logger_name=''):
    logging.config.fileConfig('app/config/logger.config', disable_existing_loggers=False)

    return logging.getLogger(logger_name)


logger = setup_logger()
