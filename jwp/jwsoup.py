import requests
# import mechanicalsoup
from bs4 import BeautifulSoup
import socks
import socket

# Configuration
SOCKS5_PROXY_HOST = '127.0.0.1'
SOCKS5_PROXY_PORT = 9050
socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)

DEFAULT_SOCKET = socket.socket
TOR_SOCKET = socks.socksocket

s = requests.Session()  # use a session for persistence

cookies = None
user_agent = 'test'


class jwsoup(object):
    cookies = None
    user_agent = 'SoupStock'
    s = requests.Session()

    def get_soup(self, url, fail=False, tor=False):
        if tor and socket.socket is not TOR_SOCKET:
            use_tor()
        elif socket.socket is not DEFAULT_SOCKET:
            reset_tor()
        req = self.s.get(
            url, headers={'User-Agent': self.user_agent},
            cookies=self.cookies)
        if req.status_code == 200 or req.status_code == 410:
            return BeautifulSoup(req.text, 'lxml')
        else:
            print('Unable to download url ' + url)
            if fail:
                raise ValueError('Status ' + str(req.status_code))
            return BeautifulSoup('', 'lxml')

    def get_cookies(self, url, tor=False):
        if tor and socket.socket is not TOR_SOCKET:
            use_tor()
        elif socket.socket is not DEFAULT_SOCKET:
            reset_tor()
        "gets cookie for passing with request otherwise site might block acces"
        req = self.s.get(
            url, headers={'User-Agent': 'jwsoup'})
        if req.status_code == 200:
            return req.cookies
        else:
            print('Unable to download url ' + url)
            return None

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


def get_soup(url, cookies=None, fail=False, tor=False):
    if tor and socket.socket is not TOR_SOCKET:
        use_tor()
    elif socket.socket is not DEFAULT_SOCKET:
        reset_tor()
    req = s.get(
        url, headers={'User-Agent': user_agent},
        cookies=cookies)
    if req.status_code == 200 or req.status_code == 410:
        return BeautifulSoup(req.text, 'lxml')
    else:
        print('Unable to download url ' + url)
        if fail:
            raise ValueError('Status ' + str(req.status_code))
        return BeautifulSoup('', 'lxml')


def get_cookies(url, tor=False):
    "gets cookie for passing with request otherwise site might block access"
    if tor and socket.socket is not TOR_SOCKET:
        use_tor()
    elif socket.socket is not DEFAULT_SOCKET:
        reset_tor()
    req = s.get(
        url, headers={'User-Agent': 'jwsoup'})
    if req.status_code == 200:
        return req.cookies
    else:
        print('Unable to download url ' + url)
        return None


def use_tor():
    "use tor proxy port"
    # Set up a proxy
    socket.socket = TOR_SOCKET


def reset_tor():
    "return to default socket"
    socket.socket = DEFAULT_SOCKET


def get_new_IP():
    pass
