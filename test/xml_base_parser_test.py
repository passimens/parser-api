import asyncio
import xml.etree.ElementTree as ElementTree
from xml_base_parser import XmlBaseParser
import unittest


async def a_pass(item):
    """Asynchronous version of pass for use in callbacks."""
    pass


class TestXmlBaseParser(unittest.IsolatedAsyncioTestCase):
    """Tests for XmlBaseParser without any interaction."""

    async def asyncSetUp(self) -> None:
        self.parser = XmlBaseParser(a_pass)
        self.fifo_path = "test_fifo"

    async def test_parse_stdin(self):
        """Tests XmlBaseParser.parse_stdin()."""
        print("trying to parse data from stdin...")
        with self.assertRaises(NotImplementedError):
            await self.parser.parse_stdin()

    async def test_parse_fifo(self):
        """Tests XmlBaseParser.parse_fifo()."""
        print(f"trying to parse data from named pipe {self.fifo_path}...")
        with self.assertRaises(NotImplementedError):
            await self.parser.parse_fifo(self.fifo_path)

    async def test_parse_line(self):
        """Tests XmlBaseParser._parse_line()."""
        with self.assertRaises(NotImplementedError):
            await self.parser._parse_line("<tag>test</tag>")

    async def test_parse_xml(self):
        """Tests XmlBaseParser._parse_xml()."""
        with self.assertRaises(NotImplementedError):
            await self.parser._parse_xml(
                "end", ElementTree.fromstring("<tag>test</tag>")
                )


class TestXmlBaseParserCustomParseXml(unittest.IsolatedAsyncioTestCase):
    """Tests for XmlBaseParser with custom _parse_xml."""

    async def _in_test_callback(self, item):
        """Callback function for use in tests."""
        self.parsed_items.append(item)

    async def asyncSetUp(self) -> None:
        async def _parser_custom_parse_xml(obj, event: str, element: ElementTree.Element):
            """Custom _parse_xml method. Will be bound to self.parser in setUp()."""
            # just pass the original xml element to the callback
            await(obj._result_callback(element))

        self.parsed_items = []
        self.parser = XmlBaseParser(self._in_test_callback)
        self.parser.__class__._parse_xml = _parser_custom_parse_xml
        self.fifo_path = "test_fifo"

    async def test_parse_xml(self):
        """Tests XmlBaseParser._parse_xml()."""
        await self.parser._parse_xml(
            "end", ElementTree.fromstring("<tag>test</tag>")
            )
        self.assertEqual(self.parsed_items[0].tag, "tag")
        self.assertEqual(self.parsed_items[0].text, "test")

    async def test_parse_line(self):
        """Tests XmlBaseParser._parse_line()."""
        await self.parser._parse_line("<tag><tag0>test0</tag0></tag>")
        await self.parser._parse_line("")
        self.assertEqual(self.parsed_items[0].tag, "tag0")
        self.assertEqual(self.parsed_items[0].text, "test0")
        self.assertEqual(self.parsed_items[1].tag, "tag")
        self.assertEqual(self.parsed_items[1].text, None)

    async def test_parse_stdin(self):
        """Tests XmlBaseParser.parse_stdin()."""
        print(
            "Parsing data from stdin... expect 2 tags, '<tag2><tag1>test1</tag1></tag2>' within 60 seconds."
            )
        waited = 0
        task = asyncio.create_task(self.parser.parse_stdin())
        while waited < 60:
            await asyncio.sleep(1)
            if len(self.parsed_items) >= 2:
                break
            waited += 1
        task.cancel()
        self.assertEqual(self.parsed_items[0].tag, "tag1")
        self.assertEqual(self.parsed_items[0].text, "test1")
        self.assertEqual(self.parsed_items[1].tag, "tag2")
        self.assertEqual(self.parsed_items[1].text, None)

    async def test_parse_fifo(self):
        """Tests XmlBaseParser.parse_fifo()."""
        print(
            f"Parsing data from named pipe {self.fifo_path}... "
            f"expect 2 tags, '<tag4><tag3>test3</tag3></tag4>' within 60 seconds."
            )
        waited = 0
        task = asyncio.create_task(self.parser.parse_fifo(self.fifo_path))
        while waited < 60:
            await asyncio.sleep(1)
            if len(self.parsed_items) >= 2:
                break
            waited += 1
        task.cancel()
        self.assertEqual(self.parsed_items[0].tag, "tag3")
        self.assertEqual(self.parsed_items[0].text, "test3")
        self.assertEqual(self.parsed_items[1].tag, "tag4")
        self.assertEqual(self.parsed_items[1].text, None)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
