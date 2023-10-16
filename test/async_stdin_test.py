from async_stdin import AsyncStdin
import unittest
import logging


class TestAsyncStdinAuto(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncStdin without any interaction."""

    def setUp(self) -> None:
        self.stdin = AsyncStdin()

    def tearDown(self) -> None:
        self.stdin.close()

    async def test_open(self):
        """Tests AsyncStdin.open() and AsyncStdin.close()."""
        self.assertTrue(self.stdin.is_closed())
        await self.stdin.open()
        self.assertFalse(self.stdin.is_closed())
        self.stdin.close()
        self.assertTrue(self.stdin.is_closed())

    async def test_reopen_opened(self):
        """Tests AsyncStdin.open() called for already opened pipe."""
        self.assertTrue(self.stdin.is_closed())
        await self.stdin.open()
        self.assertFalse(self.stdin.is_closed())
        with self.assertRaises(RuntimeError):
            await self.stdin.open()

    async def test_reopen_closed(self):
        """Tests AsyncStdin.open() called twice."""
        self.assertTrue(self.stdin.is_closed())
        await self.stdin.open()
        self.assertFalse(self.stdin.is_closed())
        self.stdin.close()
        self.assertTrue(self.stdin.is_closed())
        with self.assertRaises(RuntimeError):
            await self.stdin.open()

    async def test_context_manager(self):
        """Tests AsyncStdin.__enter__() and AsyncStdin.__exit__()."""
        self.assertTrue(self.stdin.is_closed())
        with await self.stdin.open():
            self.assertFalse(self.stdin.is_closed())
        self.assertTrue(self.stdin.is_closed())


class TestAsyncStdinInteractive(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncStdin with interaction with stdin."""

    def setUp(self) -> None:
        self.stdin = AsyncStdin()

    def tearDown(self) -> None:
        self.stdin.close()

    async def test_read_using_with(self):
        """Tests AsyncStdin _reader within context manager."""
        with await self.stdin.open() as stdin_reader:
            print("waiting for data from stdin... expect 'abcdefg'")
            self.assertEqual(await stdin_reader.readline(), b"abcdefg\n")


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
