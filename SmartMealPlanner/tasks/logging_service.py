import logging
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

LOG_FILE = BASE_DIR / "smartmeal.log"


# Configure logger
logger = logging.getLogger("SmartMeal")

logger.setLevel(logging.INFO)


if not logger.handlers:

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


# Log ingredient addition
def log_add(name, quantity, unit):

    logger.info(
        f"ADD | Ingredient: {name} | "
        f"Quantity: {quantity} {unit}"
    )


# Log ingredient update
def log_update(name, old_quantity, new_quantity):

    logger.info(
        f"UPDATE | Ingredient: {name} | "
        f"Old Quantity: {old_quantity} | "
        f"New Quantity: {new_quantity}"
    )


# Log ingredient deletion
def log_delete(name):

    logger.info(
        f"DELETE | Ingredient: {name}"
    )