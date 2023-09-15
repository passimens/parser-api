#!/usr/bin/env python3
import logging
from typing import Tuple
import asyncio
from asyncio import StreamReader, ReadTransport

logger = logging.getLogger(__name__)


async def get_stream_reader(pipe) -> Tuple[StreamReader, ReadTransport]:
    """Creates asyncio StreamReader object for a given file-like object."""

    logger.info("get_stream_reader invoked")
    logger.debug(f"for pipe = {pipe}.")

    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader(loop=loop)
    protocol = asyncio.StreamReaderProtocol(reader)
    transport, _ = await loop.connect_read_pipe(lambda: protocol, pipe)

    logger.debug(f"reader = {reader}.")

    return reader, transport
