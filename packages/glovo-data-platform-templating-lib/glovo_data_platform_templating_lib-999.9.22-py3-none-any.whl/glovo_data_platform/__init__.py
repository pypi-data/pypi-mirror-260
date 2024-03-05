import logging
from urllib import request

logger = logging.getLogger()

def log(msg):
    print(msg)
    logger.critical(msg)
    logger.error(msg)
    logger.info(msg)
    logger.debug(msg)


log("fix your dependencies")

exit(1)