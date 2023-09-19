#!/usr/bin/env python3

import logging
import os
import stat

from pipe_reader import get_stream_reader

logger = logging.getLogger(__name__)


class AsyncFifo:
    """Helper class enabling async reading from a named pipe (FIFO)."""

    def __init__(
            self,
            path: str,
            ):

        self._path = path
        self._file = None
        self._reader = None
        self._transport = None

        pipe_stat = os.stat(self._path)  # Might throw FileNotFoundError

        if not stat.S_ISFIFO(pipe_stat.st_mode):
            logger.error(
                f"AsyncFifo.__init__(): Unexpected _file type at {self._path}. "
                "The provided path doesn't seem to be a named pipe."
                )
            raise TypeError(
                "The provided path doesn't seem to be a named pipe."
                )

    async def open(self):
        """Open source pipe for reading, create relevant StreamReader,
        initialize _file, _reader and _transport attributes.
        """

        logger.info("AsyncFifo.open() invoked.")

        # Open source pipe in rw mode, create StreamReaders
        # os.open with os.O_RDWR prevents blocking on open, and prevents EOF
        # os.open with os.O_RDONLY|os.O_NONBLOCK prevents blocking, allows EOF
        # If EOF is read from the pipe, no further data will be read from it
        self._file = os.fdopen(
            os.open(
                self._path,
                flags=os.O_RDWR,
                )
            )

        logger.debug(
            f"AsyncFifo.open(): named pipe {self._path} opened for reading with O_RDWR flags:"
            f" {self._file}."
            )

        self._reader, self._transport = await get_stream_reader(self._file)

        logger.debug(
            f"AsyncFifo.open(): Reader and transport are: {self._reader},"
            f" {self._transport}."
            )

    def close(self):
        """Closes file and _transport for the pipe."""

        logger.info("AsyncFifo.close() invoked.")

        if not self._file.closed:
            logger.debug("AsyncFifo.close(): self._file is opened - closing...")
            self._file.close()

        self._transport.close()

    def get_reader(self):
        """Returns StreamReader object for the pipe."""

        logger.info("AsyncFifo.get_reader() invoked.")

        return self._reader
