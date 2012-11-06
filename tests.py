__author__ = 'IGulyaev'

import unittest, re, main

ERR_MSG = "Converted sql doesn't match to expected one:\nActual: [%s]\nExpected: [%s]"

class SqlFormatterTests(unittest.TestCase):

    def setUp(self):
        self.pattern = main.SELECT_PATTERN

    def test_basic_select_from_query_single_line(self):
        query = 'select * from schema.table'
        expected = '"select * "\n+ "from schema.table "\n'
        actual = main.sql_converter(query)
        self.assertEqual(actual, expected, \
            msg=ERR_MSG % (actual, expected))

if __name__ == '__main__':
    unittest.main()