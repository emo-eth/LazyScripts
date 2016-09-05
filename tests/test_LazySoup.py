import unittest
from LazyScripts.LazyTor import TorConnection
from LazyScripts import LazySoup
try:
    from torrc_password import PASSWORD
except:
    print('No torrc password found. Tests will fail.')


class soupTest(unittest.TestCase):

    def test_tor(self):
        LazySoup.PASSWORD = PASSWORD
        ip = 'http://icanhazip.com'
        without_tor = LazySoup.get_soup(ip).text
        with_tor = LazySoup.get_soup(ip, tor=True).text
        self.assertNotEqual(without_tor, with_tor)
        # close TorConnection
        with TorConnection(password=PASSWORD):
            pass

    @unittest.expectedFailure
    def test_fail(self):
        LazySoup.get_soup('http://123fakestre.et')

    def test_berkeley(self):
        goog = LazySoup.get_soup('http://berkeley.edu')
        self.assertTrue(goog)


if __name__ == '__main__':
    unittest.main()
