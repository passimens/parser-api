import sys
from base_parser import BaseParser
from pipe_reader import get_stream_reader
import unittest


async def a_pass(item):
    """Asynchronous version of pass for use in callbacks."""
    pass


async def a_print(item):
    """Asynchronous version of print for use in callbacks."""
    print(item)


class TestBaseParser(unittest.IsolatedAsyncioTestCase):
    """Tests for BaseParser without any interaction."""

    async def asyncSetUp(self) -> None:
        self.parser = BaseParser(a_pass)
        self.stdin_reader, _ = await get_stream_reader(sys.stdin)
        self.fifo = "test_fifo"

    async def test_parse_stream(self):
        """Tests BaseParser.parse_stream()."""
        print("trying to parse data from stdin...")
        with self.assertRaises(NotImplementedError):
            await self.parser.parse_stream(self.stdin_reader)

    async def test_parse_fifo(self):
        """Tests BaseParser.parse_fifo()."""
        print(f"trying to parse data from named pipe {self.fifo}...")
        with self.assertRaises(NotImplementedError):
            await self.parser.parse_fifo(self.fifo)

    async def test_parse_line(self):
        """Tests BaseParser._parse_line()."""
        with self.assertRaises(NotImplementedError):
            await self.parser._parse_line("test_line")
