import unittest
import requests
from jwp.LazyTor import TorConnection, check_ip

# Weird SIGALRM warnings seemed to be a quirk of unittest

CHECK_URL = 'http://icanhazip.com'


class torTest(unittest.TestCase):

    def test_tor_connection(self):
        '''Test that using a TorConnection results in a new ip'''
        start_ip = check_ip(requests)
        with TorConnection():
            session = TorConnection.Session()
            tor_ip = check_ip(session)
            self.assertNotEqual(start_ip, tor_ip)

    def test_renew(self):
        '''Test that a TorConnection can renew and get a new ip'''
        with TorConnection() as t:
            session = t.Session()
            start_ip = check_ip(session)
            t.renew()
            end_ip = check_ip(session)
            self.assertNotEqual(start_ip, end_ip)


if __name__ == '__main__':
    unittest.main()
