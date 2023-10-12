#!/usr/bin/env python3
import logging
from typing import List, Callable, Awaitable, Any

import asyncio
from async_fifo import AsyncFifo

logger = logging.getLogger(__name__)


class BaseParser:
    """A base class for parsers. Parses text and passes it to _parse_line method
    which should be implemented by subclasses.
    """

    def __init__(self, result_callback: Callable[[List[Any]], Awaitable[None]]):
        self._result_callback = result_callback

    async def _parse_line(self, line: str):
        """Parses a single line of data. Should be implemented by subclasses."""
        raise NotImplementedError

    async def parse_stream(
            self,
            pipe: asyncio.StreamReader,
            encoding: str = "latin1",
            ) -> None:
        """Main class method. Parses a stream of data from a pipe."""

        logger.info("parse_stream() invoked.")
        while True:
            data = await pipe.readline()
            if len(data) == 0:  # EOF reached
                break

            logger.debug(f"next line to parse: '{data}'")
            line = data.decode(encoding).rstrip('\n')
            await self._parse_line(line)

        logger.info("parse_stream() finished.")

    async def parse_fifo(
            self,
            fifo_path: str,
            ) -> None:
        """Reads a stream of data from a named pipe and forwards it to parse_stream.
        """
        logger.info("parse_fifo() invoked.")
        logger.debug(f"for fifo_path = {fifo_path}.")

        fifo = AsyncFifo()
        with await fifo.open(fifo_path) as reader:
            await self.parse_stream(reader)

        logger.info("parse_fifo() finished.")
