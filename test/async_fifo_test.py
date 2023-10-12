from async_fifo import AsyncFifo
import unittest


class TestAsyncFifo(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncFifo."""

    async def test_open_close(self):
        """Tests AsyncFifo.open() and AsyncFifo.close()."""
        fifo = AsyncFifo("test_fifo")
        self.assertTrue(fifo.is_closed())
        await fifo.open()
        self.assertFalse(fifo.is_closed())
        fifo.close()
        self.assertTrue(fifo.is_closed())

    async def test_context_manager(self):
        """Tests AsyncFifo.__enter__() and AsyncFifo.__exit__()."""
        fifo = AsyncFifo("test_fifo")
        self.assertTrue(fifo.is_closed())
        with await fifo.open():
            self.assertFalse(fifo.is_closed())
        self.assertTrue(fifo.is_closed())

    async def test_read_using_with(self):
        """Tests AsyncFifo reader within context manager."""
        fifo = AsyncFifo("test_fifo")
        with await fifo.open() as fifo_reader:
            print("waiting for data via named pipe test_fifo... expect 'gfedcba'")
            self.assertEqual(await fifo_reader.readline(), b"gfedcba\n")

    async def test_file_not_found(self):
        """Tests AsyncFifo.open() with non-existent file."""
        with self.assertRaises(FileNotFoundError):
            fifo = AsyncFifo("non_existent_fifo")

    async def test_not_a_fifo(self):
        """Tests AsyncFifo.open() with file that is not a FIFO."""
        with self.assertRaises(TypeError):
            fifo = AsyncFifo("not_a_fifo")


if __name__ == "__main__":
    unittest.main()
