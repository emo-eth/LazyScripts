# Summary

Convenient functions for Python. Full docs pending, but here's an overview:
- LazyCSV: reading and writing CSVs in a single line. Supports reading namedtuples and writing lists-of-like-dicts
- LazyJSON: reading and writing JSON in a single line
- LazyMultithread: multithreading and multiprocessing single functions in a single line, with error handling and traceback printing
- LazySoup: downloading webpages as BeautifulSoup objects without drama using a `requests` session. Supports routing requests through tor with `LazyTor`.
- LazyTor: Start and end Tor processes with very little hassle. Create a new connection with `connection = TorConnection()` Get a pre-configured `requests.Session` with `connection.Session()`. Get a new IP address for an existing connection with `connection.renew()`. Host multiple processes by passing in different ports to the constructor: `connection = TorConnection(socks_port=xxxx, control_port=yyyy)`. Use `connection.close()` to end the process. Supports context management, ie. `with TorConnection() as connection:` will terminate a tor process automatically when you're done using it.

# Installation

Install with `pip install lazyscripts`.

## Other Packages
- [Tor](https://www.torproject.org/docs/tor-doc-osx.html.en) - `brew install tor` with Homebrew or `sudo port install tor` with Macports on OS X
