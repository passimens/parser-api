#!/bin/bash

rm test_fifo
mkfifo test_fifo

echo 'abcdefg' | PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest pipe_reader_test.TestGetStreamReader.test_get_stdin_reader

echo 'gfedcba' > test_fifo &
PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest pipe_reader_test.TestGetStreamReader.test_get_fifo_reader

rm test_fifo
