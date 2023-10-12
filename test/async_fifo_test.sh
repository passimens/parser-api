#!/bin/bash


echo 'gfedcba' > test_fifo &
PYTHONPATH={$PYTHONPATH}:`pwd`/.. python3 -m unittest async_fifo_test.TestAsyncFifo.test_read_using_with

PYTHONPATH={$PYTHONPATH}:`pwd`/.. python3 -m unittest async_fifo_test.TestAsyncFifo.test_open_close async_fifo_test.TestAsyncFifo.test_context_manager async_fifo_test.TestAsyncFifo.test_file_not_found async_fifo_test.TestAsyncFifo.test_not_a_fifo

