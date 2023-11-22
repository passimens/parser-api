#!/bin/bash

PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest async_fifo_test.TestAsyncFifoAuto

echo 'gfedcba' > test_fifo &
PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest async_fifo_test.TestAsyncFifoInteractive


