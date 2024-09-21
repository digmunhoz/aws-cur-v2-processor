import logging

from config.settings import Settings

logging.basicConfig(
    format="%(asctime)s %(threadName)s %(levelname)-5s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO if not Settings.DEBUG else logging.DEBUG,
)
