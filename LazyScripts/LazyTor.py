import requests
from time import sleep
from stem import Signal
from stem.control import Controller
from stem.process import launch_tor
from stem.util.connection import is_valid_ipv4_address, is_valid_port
from stem.socket import ControlPort

'''TODO: Add support for different tor ports?'''

CHECK_URL = 'http://icanhazip.com'
PASSWORD = None  # torrc password
# CONTROL_PORT = 9051  # reassign as necessary

# try to import torrc password
try:
    import torrc_password
    PASSWORD = torrc_password.PASSWORD
except:
    print('Unable to load password.py with torrc password. You can still pass'
          ' it manually into the TorConnection constructor')


def check_ip(session):
    "Returns JSON response containing origin IP address."
    return session.get(CHECK_URL).text


class CurrentConnectionController(Controller):
    """Subclass of stem.control.Controller that connects to current tor
    session with default address/control_port, tries to send SIGTERM message
    to tor on exit"""

    def __init__(self, control_port, password=PASSWORD):
        address = '127.0.0.1'
        if not is_valid_ipv4_address(address):
            raise ValueError("Invalid IP address: %s" % address)
        elif not is_valid_port(control_port):
            raise ValueError("Invalid port: %s" % control_port)

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
        except Exception as e:
            print("Failed to terminate process.")
            print(type(e), e)
        self.close()


class TorConnection(object):
    PROXIES = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    CONTROL_PORT = 9051
    PASSWORD_ = PASSWORD

    def __init__(self, control_port=CONTROL_PORT, password=PASSWORD):
        self.CONTROL_PORT = control_port
        self.PASSWORD_ = password
        self.connection = self.connect()

    @staticmethod
    def connect():
        '''Returns controller for new or existing tor process.'''
        try:
            launch_tor(timeout=None)
        except OSError:  # unable to connect to 9050, eg, tor is running
            pass
        return CurrentConnectionController(TorConnection.CONTROL_PORT)

    @staticmethod
    def renew():
        '''Signal TOR for a new connection

        thanks http://stackoverflow.com/questions/30286293/
            make-requests-using-python-over-tor
        and https://gist.github.com/
            KhepryQuixote/46cf4f3b999d7f658853'''
        SLEEPSECS = 1
        SESSION = TorConnection.Session()
        old_ip = check_ip(SESSION)
        # we don't want a CCC because it closes tor session by default :)
        with Controller.from_port(port=TorConnection.CONTROL_PORT) \
                as controller:
            controller.authenticate(password=TorConnection.PASSWORD_)
            controller.signal(Signal.NEWNYM)
        new_ip = check_ip(SESSION)
        seconds = 0
        while old_ip == new_ip:
            # sleep this thread
            # for the specified duration
            sleep(SLEEPSECS)
            # track the elapsed seconds
            seconds += SLEEPSECS
            # obtain the current IP address
            new_ip = check_ip(SESSION)
            # signal that the program is still awaiting a different IP address
            print("%d seconds elapsed awaiting a different IP address."
                  % seconds)

    @staticmethod
    def close():
        '''Sends Signal.TERM to current connection'''
        try:
            CurrentConnectionController(TorConnection.CONTROL_PORT,
                                        TorConnection.PASSWORD_).SIGTERM()
        except:
            print('No current tor session.')

    @staticmethod
    def kill():
        '''Sends Signal.KILL to current connection'''
        try:
            CurrentConnectionController(TorConnection.CONTROL_PORT,
                                        TorConnection.PASSWORD_).SIGKILL()
        except:
            print('No current tor session.')

    @staticmethod
    def Session():
        '''Returns a requests.Session object configured with TorConnection's
        PROXIES class-property'''

        # create a tor connection if not already; close connection object..?
        TorConnection.connect().close()
        s = requests.Session()
        s.proxies = TorConnection.PROXIES
        return s

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
