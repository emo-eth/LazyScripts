# Summary

Convenient functions for Python:
- LazyCSV: reading and writing CSVs in a single line. Supports reading namedtuples and writing lists-of-like-dicts
- LazyJSON: reading and writing JSON in a single line
- LazyMultithread: multithreading and multiprocessing single functions in a single line, with error handling and traceback printing
- LazySoup: downloading webpages as BeautifulSoup objects without drama using a `requests` session. Supports routing requests through tor with `LazyTor`.
- LazyTor: Start and end Tor connections to use with `requests`. Get a pre-configured `requests.Session` with `TorConnection().Session()`. Get a new IP address for an existing connection with `connection.renew()`. Don't forget to `connection.close()` to end your Tor process. Supports context management, ie. `with TorConnection() as connection:` to terminate a tor process automatically when you're done using it.

# Installation

Install with `pip install lazyscripts`.

## Other Packages
- [Tor](https://www.torproject.org/docs/tor-doc-osx.html.en) - `brew install tor` with Homebrew or `sudo port install tor` with Macports on OS X

### `torrc` config

Follow [these instructions](https://stem.torproject.org/tutorials/the_little_relay_that_could.html) to set up your `torrc` for remote access with Python. Likely contenders for `torrc` location: `/etc/tor/torrc`, `/etc/torrc`, or `/usr/local/etc/tor/torrc` if you compiled from source.  
To use your `torrc` password by default, include a python module named `torrc_password.py` with the variable `PASSWORD` set to your password in the directory you are developing in.
