import unittest
import requests
from LazyScripts.LazyTor import TorConnection, check_ip


class torTest(unittest.TestCase):

    def test_tor_connection(self):
        '''Test that using a TorConnection results in a new ip'''
        start_ip = check_ip(requests)
        with TorConnection() as t:
            session = t.Session()
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

    def test_different_ports(self):
        '''Tests that a TorConnection can start on different SocksPort+Control
        Port'''
        start_ip = check_ip(requests)
        with TorConnection(socks_port=9999, control_port=10000) as t:
            session = t.Session()
            tor_ip = check_ip(session)
            self.assertNotEqual(start_ip, tor_ip)

    def test_connect_to_running_process(self):
        '''Tests that LazyTor can make a connection to a Tor process that is
        already running'''

        TorConnection()
        with TorConnection():
            pass
        self.assertTrue(True)

    def test_two_different_tor_connections(self):
        '''Test that a TorConnection on a different port has a different ip
        address'''
        with TorConnection() as t1:
            session1 = t1.Session()
            first_ip = check_ip(session1)
            with TorConnection(socks_port=1111, control_port=2222) as t2:
                session2 = t2.Session()
                second_ip = check_ip(session2)
        self.assertNotEqual(first_ip, second_ip)


if __name__ == '__main__':
    unittest.main()
