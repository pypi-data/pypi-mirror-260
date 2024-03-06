import loguru
import sys


def config_logger():
    appName = "seSql"
    logLevel = "INFO"
    config = {
        "handlers": [
            {"sink": sys.stdout, "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {extra[app]} | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>", "level": logLevel},
            # {"sink": sys.stdout, "format": "<blue>{extra[app]}</blue> | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>", "level": logLevel},
        ],
        "extra": {"app": appName}
    }
    loguru.logger.remove()
    loguru.logger.configure(**config)
    return loguru.logger


logger = config_logger()
