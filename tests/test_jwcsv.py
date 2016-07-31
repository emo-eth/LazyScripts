import unittest
import os
from jwp.jwcsv import *


class csvTest(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.testpath = self.cwd + '/testdata/test.csv'
        self.rows = [['fruit', 'count'],
                     ['banana', '5'],
                     ['apple', '4']]

    def tearDown(self):
        if os.path.isfile(self.testpath):
            os.remove(self.testpath)

    def test_read_csv(self):
        example = read_csv(self.cwd + '/testdata/example.csv')
        self.assertTrue(len(example) == 3)
        self.assertEqual(example[0][0], 'fruit')
        self.assertEqual(example[1][0], 'blanabba')

    def test_read_csv_named(self):
        example = read_csv(self.cwd + '/testdata/example.csv', named=True)
        self.assertTrue(len(example) == 2)
        self.assertEqual(example[0].fruit, 'blanabba')
        self.assertEqual(int(example[1].count), 3)
        self.assertEqual(example[0]._fields, ('fruit', 'count'))

    def test_write_csv(self):
        write_csv(self.testpath, self.rows)
        self.assertTrue(os.path.isfile(self.testpath))
        read = read_csv(self.testpath)
        self.assertEqual(read, self.rows)

    def test_write_headers(self):
        headers = self.rows[0]
        rows = self.rows[1:]
        write_csv(self.testpath, rows, headers=headers)
        self.assertTrue(os.path.isfile(self.testpath))
        read = read_csv(self.testpath)
        self.assertEqual(read, self.rows)

    def test_write_delimiter(self):
        write_csv(self.testpath, self.rows, delimiter='\t')
        self.assertTrue(os.path.isfile(self.testpath))
        read = read_csv(self.testpath, delimiter='\t')
        self.assertEqual(read, self.rows)

    def test_unicode(self):
        newrow = ['🍆', '69']
        rowcopy = self.rows.copy()
        rowcopy.append(newrow)
        write_csv(self.testpath, rowcopy)
        self.assertTrue(os.path.isfile(self.testpath))
        read = read_csv(self.testpath)
        self.assertEqual(read, rowcopy)

    def test_write_dict(self):
        rows = [{'fruit': 'blanabba', 'count': '5'},
                {'fruit': 'peesh', 'count': '3'}]
        write_csv(self.testpath, rows)
        example = read_csv(self.testpath, named=True)
        self.assertTrue(len(example) == 2)
        self.assertEqual(example[0].fruit, 'blanabba')
        self.assertEqual(int(example[1].count), 3)
        self.assertTrue(all(x in example[0]._fields for x in('fruit', 'count')))

if __name__ == '__main__':
    unittest.main()
