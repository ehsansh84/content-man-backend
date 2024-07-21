import logging


def create_logger(name, level=logging.INFO):
    import os
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not os.path.exists(f'{root_dir}/logs/'):
        os.makedirs(f'{root_dir}/logs/')
    file_handler = logging.FileHandler(f'{root_dir}/logs/{name}.log')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger_exceptions = create_logger('exceptions')
logger_handlers = create_logger('handlers')
logger_bots = create_logger('bots')
