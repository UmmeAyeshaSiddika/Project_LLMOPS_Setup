import os
import logging
from datetime import datetime
import structlog

class CustomLogger:
    def __init__(self, log_dir="logs"):
        # This finds the absolute path of the 'Project_LLMOPS_Setup' folder
        # by going up one level from where this file (logger/custom_logger.py) lives.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.abspath(os.path.join(current_dir, ".."))
        
        self.logs_dir = os.path.join(self.project_root, log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)

        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        self.log_file_path = os.path.join(self.logs_dir, log_file)

    def get_logger(self, name=None):
        # Use provided name or default to the file calling it
        logger_name = name if name else "root"

        # Standard logging configuration (Core setup)
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[
                logging.FileHandler(self.log_file_path),
                logging.StreamHandler()
            ]
        )

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger(logger_name)

# --- Auto-instantiate for the GLOBAL_LOGGER ---
# This ensures that 'from logger import GLOBAL_LOGGER' works immediately
GLOBAL_LOGGER = CustomLogger().get_logger("GLOBAL_LOGGER")

if __name__ == "__main__":
    GLOBAL_LOGGER.info("Logger initialized successfully!", root_dir=os.getcwd())