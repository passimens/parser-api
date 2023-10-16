#!/usr/bin/env python3
import asyncio
import logging
import os
import sys

from pipe_reader import get_stream_reader

logger = logging.getLogger(__name__)

class AsyncStdin:
    """Helper class enabling async reading from sys.stdin."""

    def __init__(self):
        self._stdin = None
        self._reader = None
        self._transport = None

    async def open(self):
        """Open sys.stdin for reading, create relevant StreamReader,
        initialize _reader and _transport attributes.
        """

        logger.info("AsyncStdin.open() invoked.")

        if not self.is_closed():
            logger.error(
                "AsyncStdin.open(): Attempted to open a pipe that is already open."
                )
            raise RuntimeError(
                "Attempted to open a pipe that is already open."
                )

        if self._stdin:
            logger.error(
                "AsyncStdin.open(): re-opening of sys.stdin is not supported."
                )
            raise RuntimeError(
                "Re-opening of sys.stdin is not supported."
                )

        try:
            self._stdin = os.fdopen(os.dup(sys.stdin.fileno()))
            logger.debug(f"self._stdin = {self._stdin!r}")
        except Exception as e:
            logger.error(
                f"AsyncStdin.open(): Failed to duplicate sys.stdin file descriptor."
                )
            raise e

        try:
            self._reader, self._transport = await get_stream_reader(self._stdin)
        except Exception as e:
            logger.error(
                f"AsyncStdin.open(): Failed to attach transport to sys.stdin."
                )
            raise e

        logger.debug(
            f"AsyncStdin.open(): Reader, and transport are: {self._reader},"
            f" {self._transport}."
            )

        return self

    def close(self):
        """Closes transport for sys.stdin."""
        logger.info("AsyncStdin.close() invoked.")
        if self._stdin and not self._stdin.closed:
            logger.debug("AsyncStdin.close(): self._stdin is opened - closing...")
            self._stdin.close()
        if self._transport:
            logger.debug("AsyncStdin.close(): self._transport is opened - closing...")
            self._transport.close()

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
