#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from typing import Union, List, Callable, Any, Awaitable
import logging

from base_parser import BaseParser

logger = logging.getLogger(__name__)


class XmlBaseParser(BaseParser):
    """An XLM parser. Parses text to XML entities and passes them to _parse_xml method
    which should be implemented by subclasses.
    """

    def __init__(
            self,
            result_callback: Callable[[List[Any]], Awaitable[None]],
            events: Union[List[str], None] = None,
            ):
        super().__init__(result_callback)
        self._xml_parser = ET.XMLPullParser(events)

    async def _parse_line(self, line: str) -> None:
        """Parses a single line of data."""
        self._xml_parser.feed(line)
        for event, element in self._xml_parser.read_events():
            logger.debug(
                f"event = {event}, element = {element}, "
                f"reconstructed xml = '{ET.tostring(element)}'"
                )
            await self._parse_xml(event, element)

    async def _parse_xml(self, event: str, element: ET.Element) -> None:
        """Parses a single XML entity. Should be implemented by subclasses."""
        raise NotImplementedError
