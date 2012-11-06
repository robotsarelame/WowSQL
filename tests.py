__author__ = 'IGulyaev'

import unittest, re, main

ERR_MSG = "Converted sql doesn't match to expected one:\nActual: [%s]\nExpected: [%s]"

class SqlFormatterTests(unittest.TestCase):

    def setUp(self):
        self.pattern = main.SELECT_PATTERN

    def test_regexp_smoke(self):
        query = 'Alphabet = "abcdefghigklmonpqrstuvwxyz"'
        actual = main.sql_converter(query)
        self.assertIsNone(actual, msg='The expected result for requested string [%s] should be None' % query)

    def test_basic_selectfrom_query_single_line_input(self):
        query = 'select * from schema.table'
        expected = '"select * "\n+ "from schema.table "\n'
        actual = main.sql_converter(query)
        self.assertEqual(actual, expected, \
            msg=ERR_MSG % (actual, expected))

    def test_basic_selectfrom_query_multiline_input(self):
        query = '\nselect * \nfrom schema.table\n'
        expected = '"select * "\n+ "from schema.table "\n'
        actual = main.sql_converter(query)
        self.assertEqual(actual, expected,\
            msg=ERR_MSG % (actual, expected))

    def test_basic_selectfrom_query_multilinespaces_input(self):
        query = '     select\n    *   \nfrom       schema.table'
        expected = '"select * "\n+ "from schema.table "\n'
        actual = main.sql_converter(query)
        self.assertEqual(actual, expected,\
            msg=ERR_MSG % (actual, expected))

if __name__ == '__main__':
    unittest.main()