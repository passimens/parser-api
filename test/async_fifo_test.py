from async_fifo import AsyncFifo
import unittest


class TestAsyncFifo(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncFifo."""

    def setUp(self) -> None:
        self.fifo = AsyncFifo()

    async def test_open_close(self):
        """Tests AsyncFifo.open() and AsyncFifo.close()."""

        self.assertTrue(self.fifo.is_closed())
        await self.fifo.open("test_fifo")
        self.assertFalse(self.fifo.is_closed())
        self.fifo.close()
        self.assertTrue(self.fifo.is_closed())

    async def test_context_manager(self):
        """Tests AsyncFifo.__enter__() and AsyncFifo.__exit__()."""
        self.fifo = AsyncFifo()
        self.assertTrue(self.fifo.is_closed())
        with await self.fifo.open("test_fifo"):
            self.assertFalse(self.fifo.is_closed())
        self.assertTrue(self.fifo.is_closed())

    async def test_read_using_with(self):
        """Tests AsyncFifo reader within context manager."""
        self.fifo = AsyncFifo()
        with await self.fifo.open("test_fifo") as fifo_reader:
            print("waiting for data via named pipe test_fifo... expect 'gfedcba'")
            self.assertEqual(await fifo_reader.readline(), b"gfedcba\n")

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


if __name__ == "__main__":
    unittest.main()
