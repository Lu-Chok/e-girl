# cwd = os.getcwd()
# print(cwd)


# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)


import logging
import logging.config

# from logging import lo import logger as lg
import logging
lg = logging.getLogger('aiogram')

lg.setLevel(logging.DEBUG)
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = lg
# logger.setLevel(logging.DEBUG)

# logger = logging.getLogger(__name__)
