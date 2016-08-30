import requests
# import mechanicalsoup
from bs4 import BeautifulSoup
import socks
import socket

# TODO: Handle Tor stuff through LazyTor, since it doesn't have this weirdness

# Configuration
SOCKS5_PROXY_HOST = '127.0.0.1'
SOCKS5_PROXY_PORT = 9050
socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)

DEFAULT_SOCKET = socket.socket
TOR_SOCKET = socks.socksocket

JWSOUP_SESSION = requests.Session()  # use a session for persistence

cookies = None
user_agent = 'jwsoup'
JWSOUP_SESSION.headers.update({'User-Agent': user_agent})


def get_soup(url, headers=None, cookies=None, timeout=None, fail=True,
             tor=False):
    _tor_check(tor)
    req = JWSOUP_SESSION.get(
        url, headers=headers, cookies=cookies, timeout=timeout)
    try:
        _check_response(req.status_code)
        return BeautifulSoup(req.text, 'lxml')
    except AssertionError:
        print('Unable to download url ' + url)
        if fail:
            raise ValueError('Status', req.status_code)
        return BeautifulSoup('', 'lxml')


def get_cookies(url, tor=False):
    "Gets cookie for passing with request."
    _tor_check(tor)
    req = JWSOUP_SESSION.get(
        url, headers={'User-Agent': user_agent})
    try:
        _check_response(req.status_code)
        return req.cookies
    except AssertionError:
        print('Unable to download url ' + url)
        return None


def set_tor_socket():
    "use tor proxy port"
    # Set up a proxy
    socket.socket = TOR_SOCKET


def reset_tor_socket():
    "return to default socket"
    socket.socket = DEFAULT_SOCKET


def get_new_IP():
    "TODO: Write this per that article"
    pass


def _tor_check(tor):
    if tor and socket.socket is not TOR_SOCKET:
        set_tor_socket()
    elif socket.socket is not DEFAULT_SOCKET:
        reset_tor_socket()


def _check_response(status_code):
    first_digit = status_code // 100
    assert first_digit in {2, 3}


'''
Experimental login method using mechanicalsoup for a project I was working on.

    def _login(self):
        browser = mechanicalsoup.Browser()
        login_page = browser.get(
            'https://www.redweek.com/signin?target=http%3A%2F%2Fwww.redweek.com%2F')
        login_form = login_page.soup.form
        login_page.soup.select('#id')[0]['value'] = self._username
        login_page.soup.select('#password')[0]['value'] = self._pw
        print("Logging in...")
        browser.submit(login_form, login_page.url)
        return browser.session.cookies
'''
