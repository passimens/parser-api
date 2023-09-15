#!/usr/bin/env python3
import logging
from typing import List, Callable, Awaitable, Any

from magritte.Magritte.MADescription_class import MADescription
import asyncio

logger = logging.getLogger(__name__)


async def a_print(item) -> None:
    """Asynchronous version of print for use in callbacks."""
    print(item)


class AbstractParser:
    results_description: List[MADescription] = []

    def __init__(self, result_callback: Callable[[List[Any]], Awaitable[None]] = a_print):
        self._result_callback = result_callback

    async def parse_stream(
            self,
            pipe: asyncio.StreamReader,
            result_callback: Callable[[List[Any]], Awaitable[None]] = a_print,
            ) -> None:
        pass


if __name__ == '__main__':
    pass
