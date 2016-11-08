import unittest
from LazyScripts import LazySoup


class soupTest(unittest.TestCase):

    @unittest.expectedFailure
    def test_fail(self):
        '''Test failure on bad url'''
        LazySoup.get_soup('http://123fakestre.et')

    def test_berkeley(self):
        '''Test that get_soup parses a webpage correctly'''
        berk = LazySoup.get_soup('http://berkeley.edu')
        copyright = berk.select('div.copyright')
        self.assertTrue(copyright)

    def test_berkeley_obj(self):
        '''Test that object's get_soup behaves the same way'''
        berk = LazySoup.LazySoup().get_soup('http://berkeley.edu')
        copyright = berk.select('div.copyright')
        self.assertTrue(copyright)


if __name__ == '__main__':
    unittest.main()
