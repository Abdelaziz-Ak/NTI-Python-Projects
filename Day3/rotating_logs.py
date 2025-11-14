from logging.handlers import RotatingFileHandler
import logging

logger = logging.getLogger("system_logger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("system.log", maxBytes=1048576, backupCount=3)
formatter = logger.formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("System started successfully.")