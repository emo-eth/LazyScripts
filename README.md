# Summary

Convenient functions and classes for:
- jwcsv: reading and writing CSVs (`UTF-8` encoded)
- jwcache: reading and writing JSON
- jwmultithreaded: multithreading with threadlocking (i.e. multiple threads can manipulate the same objects, via multiprocessing.pool.ThreadPool)
- jwprint: printing non-unicode characters without errors, though its functionality isn't complete for recursive datastructures (e.g. lists of lists). This also isn't necessary if your PITHONIOENCODING environment variable is set to `UTF-8` or similar.

# Requirements

- [Requests](http://docs.python-requests.org/en/master/user/install/)