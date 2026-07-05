import logging
import os

def setup_logger():
    log_filename = "pipeline.log"

    # Logger instance creation
    logger = logging.getLogger("smart_transit_logger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Format creation ('Timestamp - Level - Message')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # Handler 1: Write into a local file
        file_handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Handler 2: Produce clean print statements to terminal
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Global logger instance
log = setup_logger()