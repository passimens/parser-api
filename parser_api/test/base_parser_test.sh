#!/bin/bash


PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParser.test_parse_line

echo 'abcdefg' | PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParser.test_parse_stdin

echo 'gfedcba' > test_fifo &
PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParser.test_parse_fifo


PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParserCustomParseLine.test_parse_line

echo -e 'abcdefg\nbcdefgh' | PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParserCustomParseLine.test_parse_stdin

echo -e 'gfedcba\nhgfedcb' > test_fifo &
PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParserCustomParseLine.test_parse_fifo

PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest base_parser_test.TestBaseParserCustomParseLine.test_parse_stream



