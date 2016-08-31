import unittest
import os
from LazyScripts.LazyJSON import *


class jsonTest(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.testpath = self.cwd + '/testdata/test.json'
        self.js = {
            '1992-12-17': {'name': 'James', 'age': 69},
            '1969-06-09': {'name': 'Hugh', 'age': 420}
        }

    def tearDown(self):
        if os.path.isfile(self.testpath):
            os.remove(self.testpath)

    def test_load_json(self):
        example = load_json(self.cwd + '/testdata/example.json')
        self.assertTrue(len(example) == 2)
        self.assertTrue(all(x in example for x in ('1992-12-17',
                                                   '1969-06-09')))

    def test_write_json(self):
        write_json(self.testpath, self.js)
        self.assertTrue(os.path.isfile(self.testpath))
        read = load_json(self.testpath)
        self.assertEqual(read, self.js)

    def test_load_json_touch(self):
        test = load_json(self.testpath, touch=True)
        self.assertTrue(os.path.isfile(self.testpath))
        test['x'] = '42'
        self.assertTrue(test['x'])

    def test_write_load_unicode(self):
        self.js['🍆'] = '666'
        write_json(self.testpath, self.js, encoding='utf-8')
        test = load_json(self.testpath, encoding='utf-8')
        self.assertEqual(self.js, test)


if __name__ == '__main__':
    unittest.main()
