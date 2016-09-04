import unittest
from LazyScripts.LazyTor import TorConnection
from LazyScripts.LazySoup import *


class soupTest(unittest.TestCase):

    def test_tor(self):
        ip = 'http://icanhazip.com'
        without_tor = get_soup(ip).text
        with_tor = get_soup(ip, tor=True).text
        self.assertNotEqual(without_tor, with_tor)
        # close TorConnection
        with TorConnection():
            pass

    @unittest.expectedFailure
    def test_fail(self):
        get_soup('http://123fakestre.et')

    def test_berkeley(self):
        goog = get_soup('http://berkeley.edu')
        self.assertTrue(goog)


if __name__ == '__main__':
    unittest.main()
