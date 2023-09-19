#!/usr/bin/env python3
import logging
from typing import List, Callable, Awaitable, Any

from magritte.Magritte.MADescription_class import MADescription
import asyncio
from pipe_reader import get_stream_reader

logger = logging.getLogger(__name__)


class BaseParser:
    results_description: List[MADescription] = []

    def __init__(self, result_callback: Callable[[List[Any]], Awaitable[None]]):
        self._result_callback = result_callback

    async def _parse_line(self, line: str):
        """Parses a single line of data. Should be implemented by subclasses."""
        raise NotImplementedError

    async def parse_stream(
            self,
            pipe: asyncio.StreamReader,
            encoding: str = "latin1",
            stop_at_eof: bool = True,
            ) -> None:
        """Main class method. Parses a stream of data from a pipe. If stop_at_eof is True,
        the method will stop parsing when the pipe is closed. Otherwise, it will wait for
        new data to arrive.
        """
        while True:
            data = await pipe.readline()
            if len(data) == 0:  # EOF reached
                if stop_at_eof:
                    break
                else:
                    await asyncio.sleep(0.1)
                    continue

            logger.debug(f"next line to parse: '{data}'")
            line = data.decode(encoding).rstrip('\n')
            await self._parse_line(line)

    async def parse_fifo(
            self,
            fifo_name: str,
            ) -> None:
        """Reads a stream of data from a named pipe and forwards it to parse_stream.
        If the named pipe is disconnected from the source -
        Should be implemented by subclasses."""
        raise NotImplementedError
