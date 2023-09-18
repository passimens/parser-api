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

    async def parse_stream(
            self,
            pipe: asyncio.StreamReader,
            ) -> None:
        """Main class method. Parses a stream of data from a pipe. Should be overridden in subclasses."""
        pass

    async def parse_file(
            self,
            file_name: str,
            ) -> None:
        """Helper method. Opens a file and passes it to parse_stream."""
        with open(file_name, 'rb') as file:
            reader, _ = await get_stream_reader(file)
            await self.parse_stream(reader)

