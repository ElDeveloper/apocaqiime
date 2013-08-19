#!/usr/bin/env python
# File created on 19 Aug 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from StringIO import StringIO
from qiime.parse import parse_mapping_file
from apocaqiime.util import apply_operation_on_mapping_file_columns
from cogent.util.unit_test import TestCase, main

class TopLevelTests(TestCase):
    def setUp(self):
        """ """
        self.data, self.headers, _ = parse_mapping_file(StringIO(MAPPING_FILE))

    def test_apply_operation_on_mapping_file_columns(self):
        # test a sum
        new_headers, new_data = apply_operation_on_mapping_file_columns(
            self.headers, self.data, ['A,B', 'A,A', 'C,D'], ['first', 'second',
            'third'])
        self.assertEquals(new_headers, ['SampleID', 'Treatment', 'Info', 'A',
            'B', 'C', 'D', 'Description', 'first', 'second', 'third'])
        self.assertEquals(new_data, RESULTING_MAPPING_FILE)


RESULTING_MAPPING_FILE = [
['s1', 'Control', 'Something', '2', '0', '2', '5','foo', '2.000000', '4.000000', '7.000000'],
['s2', 'Control', 'Data', '4', '9', '1', '12223', 'bar', '13.000000', '8.000000', '12224.000000'],
['s3', 'High', 'More', '9', '8', '-4', '4', 'bas', '17.000000', '18.000000', '0.000000'],
['s4', 'Low', 'Data', '9', '6', '0.23', '6', 'spam', '15.000000', '18.000000', '6.230000'],
['s5', 'High', 'Table', '-0.234512', '4', '8', '0.00000001', 'ham', '3.765488', '-0.469024', '8.000000'],
['s6', 'Low', 'Chair', '2', '5', '1', '8', 'eggs', '7.000000', '4.000000', '9.000000'],
['s7', 'Low', 'Couch', '7', '1', '5', '0', 'beans', '8.000000', '14.000000', '5.000000']]


MAPPING_FILE = """#SampleID\tTreatment\tInfo\tA\tB\tC\tD\tDescription
s1\tControl\tSomething\t2\t0\t2\t5\tfoo
s2\tControl\tData\t4\t9\t1\t12223\tbar
s3\tHigh\tMore\t9\t8\t-4\t4\tbas
s4\tLow\tData\t9\t6\t0.23\t6\tspam
s5\tHigh\tTable\t-0.234512\t4\t8\t0.00000001\tham
s6\tLow\tChair\t2\t5\t1\t8\teggs
s7\tLow\tCouch\t7\t1\t5\t0\tbeans"""


if __name__ == "__main__":
    main()