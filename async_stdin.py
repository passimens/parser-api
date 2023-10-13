#!/usr/bin/env python3

import logging
import sys

from pipe_reader import get_stream_reader

logger = logging.getLogger(__name__)


class AsyncStdin:
    """Helper class enabling async reading from sys.stdin."""

    # Singleton pattern to prevent closing and reopening of sys.stdin
    @staticmethod
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(AsyncStdin, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_reader'):
            return
        self._reader = None
        self._transport = None

    async def open(self):
        """Open sys.stdin for reading, create relevant StreamReader,
        initialize _reader and _transport attributes.
        """

        logger.info("AsyncStdin.open() invoked.")

        if not self.is_closed():
            return self

        try:
            self._reader, self._transport = await get_stream_reader(sys.stdin)
        except Exception as e:
            logger.error(
                f"AsyncStdin.open(): Failed to attach transport to sys.stdin."
                )
            raise e

        logger.debug(
            f"AsyncStdin.open(): Reader and transport are: {self._reader},"
            f" {self._transport}."
            )

        return self

    def close(self):
        """Closes transport for sys.stdin."""
        pass  # we don't want to close sys.stdin

    def is_closed(self):
        """Returns True if file and transport are closed, False otherwise."""
        return not self._transport or self._transport.is_closing()

    def __enter__(self):
        """Async context manager entry point."""
        logger.info("AsyncStdin.__enter__() invoked.")
        return self._reader

    def __exit__(self, exc_type, exc, tb):
        """Async context manager exit point."""
        logger.info("AsyncStdin.__exit__() invoked.")
        self.close()
        return False

    @property
    def reader(self):
        """Returns StreamReader object for sys.stdin."""
        return self._reader
