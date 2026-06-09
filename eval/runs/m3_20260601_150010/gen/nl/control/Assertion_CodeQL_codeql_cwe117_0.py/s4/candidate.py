import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

username = "user123"
logger.warning(username)
