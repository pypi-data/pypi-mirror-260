import sys

from loguru import logger


class HomesolarApp:

    def __init__(self, config, production=True):
        if config is None or config == {}:
            raise Exception(
                "Server configuration cannot be empty. Please verify your server configuration before continuing!")

        self.config = config
        self.production = production

    def setup_config(self):
        pass

    def setup_logger(self):
        if self.production:
            # Remove default logger
            logger.remove()

            # Add new logger with INFO and WARNING level for stderr
            logger.add(sys.stderr, level="INFO")
            logger.add(sys.stderr, level="WARNING")

        # Setup logfiles
        logger.add(self.config["LOGGER"]["log_location"] + "DEBUG/debug_{time}.log", rotation="100 MB",
                   retention="3 days", level="DEBUG")
        logger.add(self.config["LOGGER"]["log_location"] + "INFO/info_{time}.log", rotation="100 MB",
                   retention="7 days", level="INFO")
        logger.add(self.config["LOGGER"]["log_location"] + "WARNING/warning_{time}.log", rotation="100 MB",
                   retention="7 days", level="WARNING")
        logger.add(self.config["LOGGER"]["log_location"] + "ERROR/error_{time}.log", rotation="100 MB",
                   retention="7 days", level="ERROR")
        logger.add(self.config["LOGGER"]["log_location"] + "CRITICAL/critical_{time}.log", rotation="100 MB",
                   retention="7 days", level="CRITICAL")
        logger.add(self.config["LOGGER"]["log_location"] + "logs_{time}.log", rotation="100 MB", retention="7 days")

    def run(self):
        self.setup_config()
        self.setup_logger()

    def run_bluetooth_service(self):
        pass

    def run_mqtt_service(self):
        pass

    def run_main_service(self):
        pass