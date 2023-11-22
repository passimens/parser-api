import logging

from parser_api.base_parser import BaseParser

logger = logging.getLogger(__name__)


class CopyParser(BaseParser):
    """A simple parser that sends all the data it receives to the callback."""

    async def _parse_line(
            self,
            line: str,
            ) -> None:
        """Parses a single line of data."""
        await self._result_callback([line])

