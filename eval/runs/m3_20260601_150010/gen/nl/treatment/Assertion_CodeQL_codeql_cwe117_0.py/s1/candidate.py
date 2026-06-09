import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

username = "john_doe"
logger.warning(f"User {username}")
