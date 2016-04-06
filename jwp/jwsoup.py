import requests
import mechanicalsoup
from bs4 import BeautifulSoup


cookies = None
user_agent = 'SoupStock'


class jwsoup(object):
    cookies = None
    user_agent = 'SoupStock'

    def get_soup(self, url, fail=False):
        req = requests.get(
            url, headers={'User-Agent': self.user_agent},
            cookies=self.cookies)
        if req.status_code == 200 or req.status_code == 410:
            return BeautifulSoup(req.text, 'lxml')
        else:
            print('Unable to download url ' + url)
            if fail:
                raise ValueError
            return BeautifulSoup('', 'lxml')

    @staticmethod
    def get_cookies(url):
        "gets cookie for passing with request otherwise site might block acces"
        req = requests.get(
            url, headers={'User-Agent': 'jwsoup'})
        if req.status_code == 200:
            return req.cookies
        else:
            print('Unable to download url ' + url)
            return None

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


def get_soup(url, cookies=None, fail=False):
    req = requests.get(
        url, headers={'User-Agent': user_agent},
        cookies=cookies)
    if req.status_code == 200 or req.status_code == 410:
        return BeautifulSoup(req.text, 'lxml')
    else:
        print('Unable to download url ' + url)
        if fail:
            raise ValueError
        return BeautifulSoup('', 'lxml')


def get_cookies(url):
    "gets cookie for passing with request otherwise site might block acces"
    req = requests.get(
        url, headers={'User-Agent': 'jwsoup'})
    if req.status_code == 200:
        return req.cookies
    else:
        print('Unable to download url ' + url)
        return None
