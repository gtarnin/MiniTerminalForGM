import logging


def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler = logging.FileHandler(filename='terminal.log', encoding='UTF8')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.NOTSET)
    logger.addHandler(handler)
    return logger
