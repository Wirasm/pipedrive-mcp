import logging

# --- Configure Logging ---
logging.basicConfig(
    level=logging.DEBUG,  # Ensure this is DEBUG for testing
    format="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
