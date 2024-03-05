"""
Logging module
"""

import logging
import os
import sys
from logging import Logger
from typing import TextIO

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET
APP_NAME, __ = os.path.splitext(os.path.basename(__name__))

_log_info = {"APP_ROOT_NAME": None, "APP_ROOT": None}

log = logging.getLogger(__name__)


def _get_application_name():
    """
    Get the name of the application that calls the logs.py _get_application_name() function
    """
    import inspect

    for i in range(len(inspect.stack())):
        frame = inspect.stack()[i]
        module = inspect.getmodule(frame[0])
        if module is None:
            continue
        if module:
            module_path = os.path.abspath(module.__file__)
            app_name = os.path.basename(os.path.dirname(module_path))
            if app_name != APP_NAME and app_name is not None:
                return app_name
    ## We didn't find anything but this pi-log app
    return APP_NAME


def set_root_level(level: int | str):
    """Set the root logger level
    Args:
        level (int | str): log level
    """
    level = val_to_level(level)
    logging.getLogger().setLevel(level)


def set_app_level(level: int | str):
    """Set the application logger level
    Args:
        level (int | str): log level
    """
    level = val_to_level(level)
    get_app_logger().setLevel(level)


def get_app_logger(level: int | str = None) -> Logger:
    """Get the application logger level"""
    if _log_info.get("APP_ROOT_NAME") is None:
        _log_info["APP_ROOT_NAME"] = _get_application_name()
        _log_info["APP_ROOT"] = getLogger(_log_info["APP_ROOT_NAME"])

    return getLogger(_log_info["APP_ROOT_NAME"], level=level)


def set_app_root(name: str, to_stdout: bool = False) -> Logger:
    """Set the root logger name.
    By default the root logger name is already set to the name of the
    module that imports the logs.py module
    Args:
        name (str): logger name
        to_stdout (bool): add stdout handler
    Returns:
        Logger: app root logger
    """
    _log_info["APP_ROOT_NAME"] = name
    log = getLogger(name)
    _log_info["APP_ROOT"] = log

    if to_stdout:
        add_textio_handler(log, sys.stdout)
    return log


def val_to_level(val: str | int) -> int:
    """Convert a string or int to a logging level
    Args:
        val (str | int): log level
    Returns:
        int: log level
    """
    if isinstance(val, str):
        oval = val
        val = val.strip()
        val = logging.getLevelName(val.upper())
        if not val or isinstance(val, str) and val.startswith("Level "):
            raise ValueError(f"invalid log level: {oval}")
    return val


def set_log_level(level: int | str, name: str = None):
    """Set logging to the specified level.
    If name not specified, set the application logger level.

    Args:
        level (int | str): log level
        name (str): logger name
    """
    level = val_to_level(level)
    if name is None:
        log = get_app_logger()
    else:
        log = logging.getLogger(name)
    log.setLevel(level)
    log.log(level, f"logging set to {level}")


def add_textio_handler(log: Logger, io: TextIO):
    """
    Add a StreamHandler to the logger that writes to the specified io object
    Args:
        log (Logger): logger
        io (TextIO): io object
    Example:
        import sys
        import logs
        log = logs.getLogger(__name__)
        logs.add_textio_handler(log, sys.stdout)
    """
    for h in log.handlers:
        if isinstance(h, logging.StreamHandler) and "stdout" in str(h):
            return
    log.addHandler(logging.StreamHandler(io))


def getLogger(name: str = None, level: int | str = None, to_stdout: bool = False) -> Logger:
    """Get a logger with the specified name. If level is specified,
        set the log level.
        Typical usage:
            import logs
            log = logs.getLogger(__name__)
            log.info("Hello log world!")
    Args:
        name (str): logger name
        level (int | str): log level
    Returns:
        Logger: logger with the specified name
    """
    log = logging.getLogger(name)
    if level is not None:
        set_log_level(level, name)
    ### add stdout to StreamHnadler if it isn't already in the handlers
    if to_stdout:
        add_textio_handler(log, sys.stdout)
    return log
