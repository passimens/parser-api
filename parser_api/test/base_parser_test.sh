#!/bin/bash

rm test_fifo
mkfifo test_fifo

PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParser.test_parse_line

echo 'abcdefg' | PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParser.test_parse_stdin

echo 'gfedcba' > test_fifo &
PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParser.test_parse_fifo


PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParserCustomParseLine.test_parse_line

echo -e 'abcdefg\nbcdefgh' | PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParserCustomParseLine.test_parse_stdin

echo -e 'gfedcba\nhgfedcb' > test_fifo &
PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParserCustomParseLine.test_parse_fifo_wait

echo -e 'gfedcba\nhgfedcb' > test_fifo &
PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParserCustomParseLine.test_parse_fifo_nowait

PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParserCustomParseLine.test_parse_stream

rm test_fifo