import os
import requests
from time import sleep
from subprocess import check_output
from stem import Signal
from stem.control import Controller
from stem.process import launch_tor_with_config
from stem.util.connection import is_valid_port
from stem.socket import ControlPort


PROXY_FORMAT = {
    'http': 'socks5://127.0.0.1:{0}',
    'https': 'socks5://127.0.0.1:{0}'
}


def check_ip(session):
    "Returns text containing origin IP address."
    return session.get('http://icanhazip.com').text


class TorConnection(object):
    '''Object that creates/connects to a tor process'''

    def __init__(self, socks_port=9050, control_port=9051,
                 password='my_password'):
        self.SOCKS_PORT = socks_port
        self.CONTROL_PORT = control_port
        self.PASSWORD = password
        self.PROXIES = self.format_proxies(socks_port)
        self.connection = self.connect(socks_port, control_port)

    @staticmethod
    def format_proxies(socks_port):
        '''Formats a dict of proxies with supplied socks_port

        Args:
            int socks_port: port # of tor connection
        '''
        proxies = dict()
        proxies['http'] = PROXY_FORMAT['http'].format(socks_port)
        proxies['https'] = PROXY_FORMAT['https'].format(socks_port)
        return proxies

    @staticmethod
    def hash_password(password):
        '''Returns the hash value for a password, used for setting controlport
        access.

        Args:
            string password: the password you want to hash

        Returns:
            string of password hash
        '''
        hashed_password = check_output(['tor', '--hash-password', password]
                                       ).strip()
        # stdout is bytes, but launch_tor_with_config expects unicode str
        return str(hashed_password, 'utf-8')

    def connect(self, socks_port=9050, control_port=9051):
        '''Returns controller for new or existing tor process.'''
        # create a data folder, path format tor_data/torXXXX where
        # XXXX is the socks_port #
        data_directory = str(socks_port)
        if not os.path.exists('tor_data'):
            os.mkdir('tor_data')
        if not os.path.exists('tor_data/' + data_directory):
            os.mkdir('tor_data/' + data_directory)

        # hash the control password, start+return the subprocess
        hashed_password = self.hash_password(self.PASSWORD)
        config = {
            'SocksPort': [socks_port],
            'ControlPort': [control_port],
            'Datadirectory': 'tor_data/' + data_directory,
            'HashedControlPassword': hashed_password
        }
        try:
            launch_tor_with_config(config, timeout=None)
        except OSError:  # unable to connect to 9050, eg, tor is running
            pass
        return _CurrentConnectionController(control_port, self.PASSWORD)

    def renew(self):
        '''Signal TOR for a new connection

        thanks http://stackoverflow.com/questions/30286293/
            make-requests-using-python-over-tor
        and https://gist.github.com/
            KhepryQuixote/46cf4f3b999d7f658853'''
        SLEEPSECS = 1
        SESSION = self.Session()
        old_ip = check_ip(SESSION)
        # we don't want a CCC because it closes tor process by default :)
        with Controller.from_port(port=self.CONTROL_PORT) \
                as controller:
            controller.authenticate(password=self.PASSWORD)
            controller.signal(Signal.NEWNYM)
        new_ip = check_ip(SESSION)
        seconds = 0
        while old_ip == new_ip:
            # sleep this thread for the specified duration
            sleep(SLEEPSECS)
            # track the elapsed seconds
            seconds += SLEEPSECS
            # obtain the current IP address
            new_ip = check_ip(SESSION)
            # signal that the program is still awaiting a different IP address
            print("%d seconds elapsed awaiting a different IP address."
                  % seconds)

    def close(self):
        '''Sends Signal.TERM to current connection'''
        try:
            _CurrentConnectionController(self.CONTROL_PORT,
                                         self.PASSWORD).SIGTERM()
        except Exception as e:
            print(type(e), e)
            print('No current tor process with control port {0}.'
                  .format(self.CONTROL_PORT))

    def kill(self):
        '''Sends Signal.KILL to current connection'''
        try:
            _CurrentConnectionController(self.CONTROL_PORT,
                                         self.PASSWORD).SIGKILL()
        except:
            print('No current tor process with control port {0}.'
                  .format(self.CONTROL_PORT))

    def Session(self):
        '''Returns a requests.Session object configured with this
        TorConnection's PROXIES'''

        session = requests.Session()
        session.proxies = self.PROXIES
        return session

    ''' Methods for context management (ie with statements) '''

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        try:
            self.connection.SIGTERM()
        except Exception as e:
            print("Failed to terminate process.")
            print(type(e), e)
        self.connection.close()

    ''' Aliases for methods '''

    term = close
    sigterm = close
    sigkill = kill
    SIGTERM = close
    SIGKILL = kill


class _CurrentConnectionController(Controller):
    '''Subclass of stem.control.Controller that connects to a tor process and
    tries to send SIGTERM message on exit

    Args:
        int control_port: control port for particular tor process
        string password: torrc password
    '''

    def __init__(self, control_port, password):
        assert is_valid_port(control_port), "Invalid port: %s" % control_port

        address = '127.0.0.1'
        cp = ControlPort(address, control_port)
        super().__init__(cp)
        self.authenticate(password=password)

    def SIGTERM(self):
        '''Send SIGTERM to tor'''
        self.signal(Signal.TERM)

    def SIGKILL(self):
        '''Send SIGKILL to tor'''
        self.signal(Signal.KILL)

    def __exit__(self, exit_type, value, traceback):
        try:
            self.SIGTERM()
        except:
            print("Failed to terminate process.")
        self.close()
