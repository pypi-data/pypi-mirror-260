import logging
from logging import handlers
from datetime import datetime
from path import ProjectPath
LOG_PATH = ProjectPath.LOG_PATH


def configure_logging(log_filename="logger"):
    log_filename = (
        f"{LOG_PATH}/{log_filename}_{datetime.now().strftime('%Y%m%d%H%M')}.log"
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s - %(threadName)s - %(module)s] - %(message)s",
        datefmt="%Y%m%d %H:%M:%S",
        handlers=[
            handlers.RotatingFileHandler(log_filename, maxBytes=1e6, backupCount=5),
            logging.StreamHandler(),
        ],
    )


# Call the function to configure logging
configure_logging()


class LogFactory:
    logger = logging.getLogger("logger")

    @classmethod
    def get_logger(cls, logger_name):
        return logging.getLogger(logger_name)

