import sys
import time
import base64
from io import BytesIO
from PIL import Image
from loguru import logger

logger.add(sys.stdout, format="[{time: YYYY-MM-DD HH:mm:ss} {level}] {message}", level="INFO")


def log_time(name: str):
    """
    Decorator to log the time taken by a function.

    Args:
        func: The function to be decorated.
        name: Name of the function

    Returns:
        A wrapper function that logs the time taken by the decorated function.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.info(f"Function '{name}' took {elapsed_time:.2f} seconds to execute.")
            return result
        return wrapper

    return decorator


def encode_image(image_path: str = None, image: Image = None):
    # In case an image path is passed, load the file in memory and encode it
    if image_path:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # In case an Image is passed, encode the image
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')
