import asyncio
import os
import sys

from pipe_reader import get_stream_reader
import unittest


class TestGetStreamReader(unittest.IsolatedAsyncioTestCase):
    """Tests for get_stream_reader."""

    async def test_get_stdin_reader(self):
        """Tests get_stream_reader with sys.stdin."""
        reader, transport = await get_stream_reader(sys.stdin)
        self.assertIsInstance(reader, asyncio.StreamReader)
        self.assertIsInstance(transport, asyncio.ReadTransport)
        print("waiting for data via stdin... expect 'abcdefg'")
        res = await reader.readline()
        self.assertEqual(res, b"abcdefg\n")

    async def test_get_fifo_reader(self):
        """Tests get_stream_reader with a named pipe."""
        try:
            os.mkfifo("test_fifo")
        except FileExistsError:
            pass

        file = os.fdopen(os.open("test_fifo", os.O_RDONLY | os.O_NONBLOCK))
        reader, transport = await get_stream_reader(file)
        self.assertIsInstance(reader, asyncio.StreamReader)
        self.assertIsInstance(transport, asyncio.ReadTransport)
        print("waiting for data via named pipe test_fifo... expect 'gfedcba'")
        res = await reader.readline()
        self.assertEqual(res, b"gfedcba\n")
        transport.close()
        file.close()


if __name__ == "__main__":
    unittest.main()
