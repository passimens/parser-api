import asyncio

from parser_api.async_fifo import AsyncFifo
import unittest


class TestAsyncFifoAuto(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncFifo without any interaction."""

    def setUp(self) -> None:
        self.fifo = AsyncFifo()

    def tearDown(self) -> None:
        self.fifo.close()

    async def test_open_close(self):
        """Tests AsyncFifo.open() and AsyncFifo.close()."""

        self.assertTrue(self.fifo.is_closed())
        await self.fifo.open("test_fifo")
        self.assertFalse(self.fifo.is_closed())
        self.fifo.close()
        self.assertTrue(self.fifo.is_closed())

    async def test_reopen_opened(self):
        """Tests AsyncFifo.open() called for already opened pipe."""
        self.assertTrue(self.fifo.is_closed())
        await self.fifo.open("test_fifo")
        self.assertFalse(self.fifo.is_closed())
        with self.assertRaises(RuntimeError):
            await self.fifo.open("test_fifo")

    async def test_reopen_closed(self):
        """Tests AsyncFifo.open() called twice."""
        self.assertTrue(self.fifo.is_closed())
        await self.fifo.open("test_fifo")
        self.assertFalse(self.fifo.is_closed())
        self.fifo.close()
        self.assertTrue(self.fifo.is_closed())
        await self.fifo.open("test_fifo")
        self.assertFalse(self.fifo.is_closed())

    async def test_context_manager(self):
        """Tests AsyncFifo.__enter__() and AsyncFifo.__exit__()."""
        self.fifo = AsyncFifo()
        self.assertTrue(self.fifo.is_closed())
        with await self.fifo.open("test_fifo"):
            self.assertFalse(self.fifo.is_closed())
        self.assertTrue(self.fifo.is_closed())

    async def test_file_not_found(self):
        """Tests AsyncFifo.open() with non-existent file."""
        self.fifo = AsyncFifo()
        with self.assertRaises(FileNotFoundError):
            await self.fifo.open("non_existent_file")

    async def test_not_a_fifo(self):
        """Tests AsyncFifo.open() with file that is not a FIFO."""
        self.fifo = AsyncFifo()
        with self.assertRaises(TypeError):
            await self.fifo.open("not_a_fifo")


class TestAsyncFifoInteractive(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncFifo with interaction with a named pipe."""

    def setUp(self) -> None:
        self.fifo = AsyncFifo()

    def tearDown(self) -> None:
        self.fifo.close()

    async def test_read_using_with(self):
        """Tests AsyncFifo _reader within context manager."""
        self.fifo = AsyncFifo()
        with await self.fifo.open("test_fifo") as fifo_reader:
            print("waiting for data via named pipe test_fifo... expect 'gfedcba'")
            self.assertEqual(await fifo_reader.readline(), b"gfedcba\n")


class TestAsyncFifoAllowEOF(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncFifo with interaction with a named pipe which allows EOF."""

    def setUp(self) -> None:
        self.fifo = AsyncFifo()

    def tearDown(self) -> None:
        self.fifo.close()

    async def test_read_until_eof(self):
        """Tests AsyncFifo _reader within context manager."""
        self.fifo = AsyncFifo()
        with await self.fifo.open("test_fifo", allow_eof=True) as fifo_reader:
            print("waiting for 1 line from named pipe test_fifo...")
            self.assertNotEqual(await fifo_reader.readline(), b"")
            print("No more data. So, next attempt to read should return empty line.")
            self.assertEqual(await fifo_reader.readline(), b"")


class TestAsyncFifoDisallowEOF(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncFifo with interaction with a named pipe which does not allow EOF."""

    def setUp(self) -> None:
        self.fifo = AsyncFifo()

    def tearDown(self) -> None:
        self.fifo.close()

    async def test_read_without_eof(self):
        """Tests AsyncFifo _reader within context manager."""
        self.fifo = AsyncFifo()
        with await self.fifo.open("test_fifo", allow_eof=False) as fifo_reader:
            print("waiting for 1 line from named pipe test_fifo...")
            self.assertNotEqual(await fifo_reader.readline(), b"")
            print("No more data. So, next attempt to read should stuck waiting for data.")
            with self.assertRaises(asyncio.TimeoutError):
                await asyncio.wait_for(fifo_reader.readline(), timeout=1)


if __name__ == "__main__":
    unittest.main()
