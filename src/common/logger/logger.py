from __future__ import annotations

import logging
import sys


class Logger:
    _instances: dict[str, Logger] = {}

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)

        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            self._logger.addHandler(handler)

    @classmethod
    def get_instance(cls, name: str, level: int = logging.INFO) -> Logger:
        if name not in cls._instances:
            cls._instances[name] = cls(name, level)
        return cls._instances[name]

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def critical(self, message: str) -> None:
        self._logger.critical(message)
