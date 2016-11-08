import requests
from bs4 import BeautifulSoup

SESSION = requests.Session()  # use a session for persistence (ie, cookies)
SESSION.headers.update({'User-Agent': 'LazySoup'})


def get_soup(url, parser='lxml', headers=None, cookies=None, timeout=None):
    '''Uses a requests.Session object to get a url and returns it as a
    BeautifulSoup object.

    Args:
        REQUIRED:
        string url: url of the page

        Optional:
        string parser: parser you wish to use for creating BeautifulSoup object
        dict headers: headers you wish to pass with request
        dict cookies: cookies you wish to pass with request
        number timeout: how long to wait before throwing an error
    '''
    req = SESSION.get(
        url, headers=headers, cookies=cookies, timeout=timeout)
    try:
        _check_response(req.status_code)
        return BeautifulSoup(req.text, parser)
    except AssertionError:
        print('Unable to download url ' + url)
        raise ValueError('Status', req.status_code)


def get_cookies(url, headers=None):
    '''Gets and returns cookies for passing with requests.

    Args:
        string url: url to get and return cookies for
        dict headers: headers to pass with the request

    Returns cookies acquired by the request.
    '''
    req = SESSION.get(url, headers=headers)
    try:
        _check_response(req.status_code)
        return req.cookies
    except AssertionError:
        print('Unable to download url ' + url)
        return None


def _check_response(status_code):
    '''Checks the first digit of a status code returned by a GET, and
    assumes/asserts any 2xx/3xx status code is ok.
    '''
    first_digit = status_code // 100
    assert first_digit in {2, 3}, "Bad status code"


'''LazySoup class'''


class LazySoup(object):
    '''A class wrapper around get_soup with its own session property, which
    allows for per-instance settings
    '''

    def __init__(self, headers={'User-Agent': 'LazySoup'},
                 session=requests.Session()):
        '''
        Args:
            Optional
            requests.Session session: the session to use for getting soup
            dict headers: dict of headers to add to self.session.headers
        '''
        self.session = session
        self.session.headers.update(headers)

    def get_soup(self, url, parser='lxml', headers=None, cookies=None,
                 timeout=None):
        '''Uses a requests.Session object to get a url and returns it as a
        BeautifulSoup object.

        Args:
            REQUIRED:
            string url: url of the page

            Optional:
            string parser: parser you wish to use for creating BeautifulSoup
                object
            dict headers: headers you wish to pass with request
            dict cookies: cookies you wish to pass with request
            number timeout: how long to wait before throwing an error
        '''
        req = self.session.get(
            url, headers=headers, cookies=cookies, timeout=timeout)
        try:
            _check_response(req.status_code)
            return BeautifulSoup(req.text, parser)
        except AssertionError:
            print('Unable to download url ' + url)
            raise ValueError('Status', req.status_code)


''' Module-level setters '''


def use_proxies_of(session):
    '''Configures module to use the proxies for a particular session
        (especially a session configured for Tor)

    Args:
        requests.Session session: a session whose proxies will be used for the
            module-level SESSION
    '''
    SESSION.proxies = session.proxies
