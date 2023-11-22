import asyncio
import logging
import sys

from parser_api.base_parser import BaseParser
from parser_api.pipe_reader import get_stream_reader

logger = logging.getLogger(__name__)


async def a_print(item) -> None:
    """Asynchronous version of print for use in callbacks."""
    print(item)


class PrinterParser(BaseParser):
    """A simple parser that prints all the data it receives."""
    def __init__(self):
        super().__init__(a_print)

    async def _parse_line(
            self,
            line: str,
            ) -> None:
        """Parses a single line of data."""
        await self._result_callback([line])


if __name__ == "__main__":

    async def main(fifo=None) -> None:
        parser = PrinterParser()
        if fifo:
            await parser.parse_fifo(fifo)
        else:
            reader, _ = await get_stream_reader(sys.stdin)
            await parser.parse_stream(reader)

    if len(sys.argv) > 1:
        src = sys.argv[1]
    else:
        src = None

    asyncio.run(main(src))
