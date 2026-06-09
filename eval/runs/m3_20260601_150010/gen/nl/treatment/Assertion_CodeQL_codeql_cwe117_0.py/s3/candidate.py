import logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# Add a handler to output logs
handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)
logger.addHandler(handler)

# Log a username at warning level
username = "example_user"
logger.warning(f"Username: {username}")
