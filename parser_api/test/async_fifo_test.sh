#!/bin/bash

rm test_fifo
mkfifo test_fifo

PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest async_fifo_test.TestAsyncFifoAuto

echo 'gfedcba' > test_fifo &
PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest async_fifo_test.TestAsyncFifoInteractive

echo 'gfedcba' > test_fifo &
PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest async_fifo_test.TestAsyncFifoAllowEOF

echo 'gfedcba' > test_fifo &
PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest async_fifo_test.TestAsyncFifoDisallowEOF

rm test_fifo
