# Summary

Convenient functions and superclasses for:
- jwcsv: reading and writing CSVs (`UTF-8` encoded)
- jwcache: reading and writing JSON
- jwsoup: downloading webpages as BeautifulSoup objects
- jwmultithreaded: multithreading with threadlocking (i.e. multiple threads can manipulate the same objects, via multiprocessing.pool.ThreadPool)
- jwprint: printing non-unicode characters without errors, though its functionality isn't complete for recursive datastructures (e.g. lists of lists). This also isn't necessary if your PITHONIOENCODING environment variable is set to `UTF-8` or similar.

# Requirements

- [Requests](http://docs.python-requests.org/en/master/user/install/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)