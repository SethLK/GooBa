# packed.py
import ast
import inspect
import sys
from functools import wraps
from .parser import transform_jsx_in_file


def view(func):
    """Decorator that enables JSX-like syntax in the function"""
    source_lines = []
    try:
        # Get the source code of the function
        source = inspect.getsource(func)
        source_lines = source.split('\n')

        # Transform JSX syntax
        transformed_source = transform_jsx_in_file(source)

        # Execute the transformed code in the function's globals
        exec(transformed_source, func.__globals__)

        # Get the transformed function
        transformed_func = func.__globals__[func.__name__]
        return transformed_func

    except (OSError, TypeError):
        # If we can't get source, return original function
        return func