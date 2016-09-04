import requests
from LazyScripts import LazyTor
from bs4 import BeautifulSoup

SESSION = requests.Session()  # use a session for persistence
TOR = False

cookies = None
user_agent = 'LazySoup'
SESSION.headers.update({'User-Agent': user_agent})


def get_soup(url, headers=None, cookies=None, timeout=None, fail=True,
             tor=TOR, session=SESSION):
    '''Uses a requests.Session object to get a url and returns it a
    BeautifulSoup object.

    Args:
        string url: url of the page
        dict headers: headers you wish to pass with request
        dict cookies: cookies you wish to pass with request
        number timeout: how long you wait before throwing an error
        bool fail: if false, returns empty bs4 object instead of raising an
            error
        bool tor: route through a tor process on port 9050 with cp 9051
            (note: will not terminate tor process)
        requests.Session session: requests.Session object used to make
            requests. It is possible to pass in a pre-configured object using
            different ports for tor.'''
    _tor_check(tor)
    req = session.get(
        url, headers=headers, cookies=cookies, timeout=timeout)
    try:
        _check_response(req.status_code)
        return BeautifulSoup(req.text, 'lxml')
    except AssertionError:
        print('Unable to download url ' + url)
        if fail:
            raise ValueError('Status', req.status_code)
        return BeautifulSoup('', 'lxml')


def get_cookies(url, tor=TOR, session=SESSION):
    '''Gets and returns cookies for passing with requests.

    Args:
        bool tor: route through a tor process on port 9050 with cp 9051
            (note: will not terminate tor process)
        requests.Session session: requests.Session object used to make
            requests. It is possible to pass in a pre-configured object using
            different ports for tor'''
    _tor_check(tor)
    req = session.get(
        url, headers={'User-Agent': user_agent})
    try:
        _check_response(req.status_code)
        return req.cookies
    except AssertionError:
        print('Unable to download url ' + url)
        return None


def _check_response(status_code):
    first_digit = status_code // 100
    assert first_digit in {2, 3}


''' Tor Functions '''


def use_proxies_of(session):
    '''Configures module to use the proxies for a particular session
        (especially a session configured for Tor)

    Args:
        requests.Session session: a session whose proxies will be used for the
            module-level SESSION
    '''
    SESSION.proxies = session.proxies


def _tor_check(tor):
    '''Configures module-level SESSION to use a tor connection's proxies if
    supplied value is True'''
    if tor and not SESSION.proxies:
        use_proxies_of(LazyTor.TorConnection().Session())
    if not tor and SESSION.proxies:
        SESSION.proxies = None
