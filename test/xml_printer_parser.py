import asyncio
import logging
import sys
from xml.etree import ElementTree

from xml_base_parser import XmlBaseParser
from pipe_reader import get_stream_reader

logger = logging.getLogger(__name__)


async def a_print(item) -> None:
    """Asynchronous version of print for use in callbacks."""
    print(item)


class XmlPrinterParser(XmlBaseParser):
    """A simple parser that prints all the XML elements it receives."""
    def __init__(self):
        super().__init__(a_print)

    async def _parse_xml(
            self,
            event: str,
            element: ElementTree.Element,
            ) -> None:
        """Parses a single line of data."""
        await self._result_callback([element])


if __name__ == "__main__":

    async def main(fifo=None) -> None:
        parser = XmlPrinterParser()
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
