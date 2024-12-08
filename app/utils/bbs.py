import base64
from loguru import logger


def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        logger.error(f"Не найдено {image_path} для base64")
        return None
    except Exception as e:  # Added general exception handling
        logger.error(f"Ошибка:\n{e}")
        return None