#!/bin/bash

PYTHONPATH={$PYTHONPATH}:`pwd`/.. python3 -m unittest async_stdin_test.TestAsyncStdinAuto

echo 'abcdefg' | PYTHONPATH={$PYTHONPATH}:`pwd`/.. python3 -m unittest async_stdin_test.TestAsyncStdinInteractive


