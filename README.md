# Summary

Convenient functions for Python:
- LazyCSV: reading and writing CSVs in a single line. Supports reading namedtuples and writing lists-of-like-dicts
- LazyJSON: reading and writing JSON in a single line
- LazyMultithread: multithreading and multiprocessing single functions in a single line, with error handling and traceback printing
- LazySoup: downloading webpages as BeautifulSoup objects without drama using a `requests` session. Supports routing network through a tor port for anonymous-ish scraping.
- LazyTor: Start and end Tor connections to use with `requests`. Get a pre-configured `requests.Session` with TorConnection.Session(). Get new IP address with `TorConnection.renew()` Supports context management, ie. `with TorConnection():` to close a Tor session automatically.

# Requirements

## Python dependencies
- [Requests](http://docs.python-requests.org/en/master/user/install/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
- [Stem](https://stem.torproject.org)

## Other Packages
- [Tor](https://www.torproject.org/docs/tor-doc-osx.html.en) - `brew install tor` with Homebrew or `sudo port install tor` with Macports on OS X

### `torrc` config

Follow [these instructions](https://stem.torproject.org/tutorials/the_little_relay_that_could.html) to set up your torrc for remote access with Python.

