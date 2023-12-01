import asyncio
from parser_api.base_parser import BaseParser
import unittest


async def a_pass(item):
    """Asynchronous version of pass for use in callbacks."""
    pass


class TestBaseParser(unittest.IsolatedAsyncioTestCase):
    """Tests for BaseParser without any interaction."""

    async def asyncSetUp(self) -> None:
        self.parser = BaseParser(a_pass)
        self.fifo_path = "test_fifo"

    async def test_parse_stdin(self):
        """Tests BaseParser.parse_stdin()."""
        print("trying to parse data from stdin...")
        with self.assertRaises(NotImplementedError):
            await self.parser.parse_stdin()

    async def test_parse_fifo(self):
        """Tests BaseParser.parse_fifo()."""
        print(f"trying to parse data from named pipe {self.fifo_path}...")
        with self.assertRaises(NotImplementedError):
            await self.parser.parse_fifo(self.fifo_path)

    async def test_parse_line(self):
        """Tests BaseParser._parse_line()."""
        with self.assertRaises(NotImplementedError):
            await self.parser._parse_line("test_line")


class TestBaseParserCustomParseLine(unittest.IsolatedAsyncioTestCase):
    """Tests for BaseParser with custom _parse_line."""

    async def _in_test_callback(self, items):
        """Callback function for use in tests."""
        self.parsed_items.extend(items)

    async def asyncSetUp(self) -> None:
        async def _parser_custom_parse_line(obj, line: str):
            """Custom _parse_line method. Will be bound to self.parser in setUp()."""
            # just pass the original line to the callback
            await obj._result_callback([line])

        self.parsed_items = []
        self.parser = BaseParser(self._in_test_callback)
        self.parser.__class__._parse_line = _parser_custom_parse_line
        self.fifo_path = "test_fifo"

    async def test_parse_line(self):
        """Tests BaseParser._parse_line()."""
        await self.parser._parse_line("test_line")
        self.assertEqual(self.parsed_items, ["test_line"])

    async def test_parse_stdin(self):
        """Tests BaseParser.parse_stdin()."""
        print("Parsing data from stdin... expect 2 lines, 'abcdefg', 'bcdefgh' within 60 seconds.")
        waited = 0
        task = asyncio.create_task(self.parser.parse_stdin())
        while waited < 60:
            await asyncio.sleep(1)
            if len(self.parsed_items) >= 2:
                break
            waited += 1
        task.cancel()
        self.assertEqual(self.parsed_items, ["abcdefg", "bcdefgh"])

    async def test_parse_fifo_wait(self):
        """Tests BaseParser.parse_fifo() with nowait=False."""
        print(
            f"Parsing data from named pipe {self.fifo_path}... expect 2 lines, 'gfedcba', 'hgfedcb' within 60 seconds."
            )
        waited = 0
        task = asyncio.create_task(self.parser.parse_fifo(self.fifo_path, nowait=False))
        while waited < 60:
            await asyncio.sleep(1)
            if len(self.parsed_items) >= 2:
                break
            waited += 1
        task.cancel()
        self.assertEqual(self.parsed_items, ["gfedcba", "hgfedcb"])

    async def test_parse_fifo_nowait(self):
        """Tests BaseParser.parse_fifo() with nowait=True (default)."""
        print(
            f"Parsing data from named pipe {self.fifo_path}... expect 2 lines, 'gfedcba', 'hgfedcb' right away."
            f"Will fail if run manually without sending data to {self.fifo_path}, "
            f"because the parse_fifo method will not wait for data."
            )
        waited = 0
        task = asyncio.create_task(self.parser.parse_fifo(self.fifo_path))
        while waited < 60:
            if task.done():
                break
            await asyncio.sleep(1)
            if len(self.parsed_items) >= 2:
                break
            waited += 1
        task.cancel()
        self.assertEqual(self.parsed_items, ["gfedcba", "hgfedcb"])

    async def test_parse_stream(self):
        """Tests BaseParser.parse_stream()."""
        print("Running a command which would return 2 lines, 'bcdefgh', 'cdefghi'.")
        proc = await asyncio.create_subprocess_shell(
            "echo 'bcdefgh\ncdefghi'",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )
        waited = 0
        task = asyncio.create_task(self.parser.parse_stream(proc.stdout))
        while waited < 10:
            await asyncio.sleep(0.1)
            if len(self.parsed_items) >= 2:
                break
            waited += 1
        task.cancel()
        self.assertEqual(self.parsed_items, ["bcdefgh", "cdefghi"])


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
