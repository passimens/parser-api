import asyncio
import logging
import sys

from base_parser import BaseParser
from pipe_reader import get_stream_reader

logger = logging.getLogger(__name__)


async def a_print(item) -> None:
    """Asynchronous version of print for use in callbacks."""
    print(item)


class PrinterParser(BaseParser):
    """A simple parser that prints all the data it receives."""
    def __init__(self):
        super().__init__(a_print)

    async def parse_stream(
            self,
            pipe: asyncio.StreamReader,
            ) -> None:
        """Main class method. Parses a stream of data from a pipe."""
        while True:
            line = await pipe.readline()
            if not line:
                break
            await self._result_callback([line])


if __name__ == "__main__":

    async def main(file=None) -> None:
        parser = PrinterParser()
        if file:
            await parser.parse_file(file)
        else:
            reader, _ = await get_stream_reader(sys.stdin)
            await parser.parse_stream(reader)

    if len(sys.argv) > 1:
        src = sys.argv[1]
    else:
        src = None

    asyncio.run(main(src))
