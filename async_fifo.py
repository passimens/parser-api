#!/usr/bin/env python3

import logging
import os
import stat

from . pipe_reader import get_stream_reader

logger = logging.getLogger(__name__)


class AsyncFifo:
    """Helper class enabling async reading from a named pipe (FIFO)."""

    def __init__(self):

        self._path = None
        self._file = None
        self._reader = None
        self._transport = None

    async def open(self, path: str):
        """Open source pipe for reading, create relevant StreamReader,
        initialize _file, _reader and _transport attributes.
        """

        logger.info("AsyncFifo.open() invoked.")

        if not self.is_closed():
            logger.error(
                "AsyncFifo.open(): Attempted to open a pipe that is already open."
                )
            raise RuntimeError(
                "Attempted to open a pipe that is already open."
                )

        pipe_stat = os.stat(path)  # Might throw FileNotFoundError

        if not stat.S_ISFIFO(pipe_stat.st_mode):
            logger.error(
                f"AsyncFifo.__init__(): Unexpected _file type at {path}. "
                "The provided path doesn't seem to be a named pipe."
                )
            raise TypeError(
                "The provided path doesn't seem to be a named pipe."
                )

        self._path = path

        try:
            # os.open with os.O_RDWR prevents blocking on open, and prevents EOF
            # os.open with os.O_RDONLY|os.O_NONBLOCK prevents blocking, allows EOF
            # If EOF is read from the pipe, no further data will be read from it
            self._file = os.fdopen(
                os.open(
                    self._path,
                    flags=os.O_RDWR,
                    )
                )
        except Exception as e:
            logger.error(
                f"AsyncFifo.open(): Failed to open named pipe {self._path} for reading."
                )
            raise e

        logger.debug(
            f"AsyncFifo.open(): named pipe {self._path} opened for reading with O_RDWR flags:"
            f" {self._file}."
            )

        try:
            self._reader, self._transport = await get_stream_reader(self._file)
        except Exception as e:
            logger.error(
                f"AsyncFifo.open(): Failed to attach transport to named pipe {self._path}."
                )
            self._file.close()
            raise e

        logger.debug(
            f"AsyncFifo.open(): Reader and transport are: {self._reader},"
            f" {self._transport}."
            )

        return self

    def close(self):
        """Closes file and transport for the pipe."""

        logger.info("AsyncFifo.close() invoked.")

        if self._file and not self._file.closed:
            logger.debug("AsyncFifo.close(): self._file is opened - closing...")
            self._file.close()

        if self._transport and not self._transport.is_closing():
            self._transport.close()

    def is_closed(self):
        """Returns True if file and transport are closed, False otherwise."""
        return (not self._file or self._file.closed) and (not self._transport or self._transport.is_closing())

    def __enter__(self):
        """Async context manager entry point."""
        logger.info("AsyncFifo.__enter__() invoked.")
        return self._reader

    def __exit__(self, exc_type, exc, tb):
        """Async context manager exit point."""
        logger.info("AsyncFifo.__exit__() invoked.")
        self.close()
        return False

    @property
    def reader(self):
        """Returns StreamReader object for the pipe."""
        return self._reader
