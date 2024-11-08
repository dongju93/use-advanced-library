# logger.py
from typing import Optional

import picologging


def get_logger(name: Optional[str] = None) -> picologging.Logger:
    """Get configured logger instance"""
    logger = picologging.getLogger(name or __name__)

    # Prevent adding handlers multiple times
    if not logger.handlers:
        logger.setLevel(picologging.DEBUG)

        # Create file handler
        file_handler = picologging.FileHandler("logs/app.log")
        file_handler.setLevel(picologging.DEBUG)

        # Create formatter
        formatter = picologging.Formatter(
            "%(created)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        # Add handler
        logger.addHandler(file_handler)

    return logger
