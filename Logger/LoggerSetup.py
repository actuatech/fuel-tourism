import logging


def setup_logger(logger_name, log_file, level=logging.INFO, stream: bool = True):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(fileHandler)
    if stream:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)