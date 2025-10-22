import functools
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s [main]: %(message)s')

def log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Called function: {func.__name__}")
        logging.info(f"Args: {args} | Kwargs: {kwargs}")

        try:
            result = func(*args, **kwargs)
            # logging.info(f"Return value: {result}")
            return result
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            logging.error(traceback.format_exc())
            raise  # Re-raise so the caller can handle it if needed

    return wrapper