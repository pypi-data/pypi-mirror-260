# Copyright 2023-2024 Parker Owan.  All rights reserved.

import logging
import functools


def logerror(func):
    """Decorator to try/catch a method and log exceptions"""

    @functools.wraps(func)
    def wrapper_func(self, **kwargs):
        try:
            func(self, **kwargs)
        except Exception as e:
            logging.error(e)

    return wrapper_func
