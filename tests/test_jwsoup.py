import unittest
from jwp.jwsoup import *


class soupTest(unittest.TestCase):

    def test_tor(self):
        ip = 'http://ifconfig.me/ip'
        without_tor = get_soup(ip).text
        with_tor = get_soup(ip, tor=True).text
        self.assertNotEqual(without_tor, with_tor)

    @unittest.expectedFailure
    def test_fail(self):
        get_soup('http://123fakestre.et')

    def test_google(self):
        goog = get_soup('http://google.com')
        self.assertTrue(goog)

if __name__ == '__main__':
    unittest.main()
