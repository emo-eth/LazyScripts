import unittest
import requests
from jwp.jwtor import TorConnection, check_ip

# with tor_connection(True):
#     print('no proxies')
#     print(check_ip())
#     SESSION.proxies = PROXIES
#     print('with proxies')
#     print(check_ip())
#     print('renewing connection')
#     renew_connection()
#     print('connection renewed')
#     print(check_ip())

# TODO: Fix weird SIGALRM warnings..? I have a hunch that it's actually
# unittest's BufferedWriter

CHECK_URL = 'http://icanhazip.com'


class torTest(unittest.TestCase):

    def test_tor_connection(self):
        '''Test that using a TorConnection results in a new ip'''
        start_ip = requests.get(CHECK_URL).text
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
