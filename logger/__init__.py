from .custom_logger import CustomLogger

# Create the specific variable model_loader.py is looking for
GLOBAL_LOGGER = CustomLogger().get_logger("GLOBAL_LOGGER")