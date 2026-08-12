import logging
import sys

def setup_logging():
    """
    Set up logging configuration for the application.
    Logs will be output to stdout with a specific format.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def get_logger(name: str)-> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name (str): The name of the logger.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(name)

