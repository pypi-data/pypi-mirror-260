import logging
import logging.config
import os
from colorlog import ColoredFormatter

from atb_lib.src.config_loader import load_config


class ColoredLogger:
    def __init__(self, config_file, logger_name):
        self._config_file = config_file
        self._logger_name = logger_name
        self._logger = None
        self.setup_logger()

    def setup_logger(self):
        """
        Set up a colored logger with configurations loaded from a JSON file.
        If the configuration file is not found, default settings are used.
        """
        if not os.path.exists(self._config_file):
            logging.warning(f"Configuration file {self._config_file} not found. Using default settings.")
            self._setup_default_logger()
        else:
            config = load_config(self._config_file)
            try:
                logging.config.dictConfig(config)
            except Exception as e:
                logging.error(f"Error in loading configuration: {e}")
                self._setup_default_logger()

        self._logger = logging.getLogger(self._logger_name)


    @staticmethod
    def _setup_default_logger():
        handler = logging.StreamHandler()
        formatter = ColoredFormatter('%(asctime)s %(module)s %(log_color)s%(levelname)s: %(message)s',
                                     datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logging.basicConfig(handlers=[handler], level=logging.INFO)

    def get_logger(self):
        """Return the configured logger."""
        return self._logger

    def debug(self, param):
        self._logger.debug(param)

    def info(self, param):
        self._logger.info(param)

    def warning(self, param):
        self._logger.warning(param)

    def error(self, param):
        self._logger.error(param)
