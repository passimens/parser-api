#!/bin/bash


PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest xml_base_parser_test.TestXmlBaseParser.test_parse_xml

PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest xml_base_parser_test.TestXmlBaseParser.test_parse_line

echo '<tag>test</tag>' | PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest xml_base_parser_test.TestXmlBaseParser.test_parse_stdin

echo '<tag>test</tag>' > test_fifo &
PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest xml_base_parser_test.TestXmlBaseParser.test_parse_fifo


PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest xml_base_parser_test.TestXmlBaseParserCustomParseXml.test_parse_xml

PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest xml_base_parser_test.TestXmlBaseParserCustomParseXml.test_parse_line

PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest xml_base_parser_test.TestXmlBaseParserCustomParseXml.test_invalid_xml

echo -e '<tag2>\n<tag1>test1</tag1>\n</tag2>' | PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest xml_base_parser_test.TestXmlBaseParserCustomParseXml.test_parse_stdin

echo -e '<tag4>\n<tag3>test3</tag3>\n</tag4>' > test_fifo &
PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest xml_base_parser_test.TestXmlBaseParserCustomParseXml.test_parse_fifo

PYTHONPATH={$PYTHONPATH}:`pwd`/../.. python3 -m unittest xml_base_parser_test.TestXmlBaseParserCustomParseXml.test_parse_stream

