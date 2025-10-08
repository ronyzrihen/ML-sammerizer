from fastapi import HTTPException
from functools import wraps
from core.logger import logger


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def handle_errors(func):
    """
    A decorator to catch unhandled exceptions in an endpoint, log them,
    and return a standard 500 internal server error response.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as he:
            raise he
        except Exception:
            logger.error("An unexpected error occurred in an endpoint:", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="An internal server error occurred. Please check the logs."
            )
    return wrapper
