from multiprocessing.pool import Pool, ThreadPool
from multiprocessing import Manager, cpu_count


class jwmultithreaded(object):
    '''Inspired by http://chriskiehl.com/article/parallelism-in-one-line/
    as well as operations that do not need to be threadsafe'''

    def __init__(self):
        self.cache_updated = False

    def multithread(self, fn, args=[[]], pool_type=Pool,
                    processes=cpu_count()):
        '''Multithread method using a Pool. Not inherently threadsafe.
        For threadsafe operations, use Managers.
        Args must be wrapped in their own list, as starmap is used for
        multiple arguments.
        Returns a list of the results'''

        with pool_type(processes) as pool:
            results = pool.starmap(fn, args)
        # close the pool and wait for results to return
        return results

    def safe_multithread(self, fn, args=[[]], processes=8):
        '''Guaranteed threadsafe version of multithread using ThreadPool.
        Limited by interpreter lock.'''

        return self.multithread(fn, args=args, pool_type=ThreadPool, processes=processes)

    def multithread_failsafe(self, fn, args=[[]], pool_type=Pool,
                             processes=cpu_count()):
        '''Aynchronous multithreading that does not break on individual errors.
        Instead, prints error and message, and the input is disregarded'''

        with pool_type(processes) as pool:
            threads = []
            for elem in args:
                threads.append(pool.apply_async(fn, elem))
            results = []
            for r in threads:
                try:
                    results.append(r.get())
                except Exception as e:
                    print(type(e), e)
        return results

    def safe_multithread_failsafe(self, fn, args=[[]], processes=8):
        '''Threadsafe version of multithread_failsafe.
        Limited by interpretor lock.'''

        return self.multithread_failsafe(fn, args=args, pool_type=ThreadPool,
                                         processes=processes)


def multithread(fn, args=[[]], pool_type=Pool,
                processes=8):
    '''Multithread method using a Pool. Not inherently threadsafe.
    For threadsafe operations, use Managers.
    Args must be wrapped in their own list, as starmap is used for
    multiple arguments.
    Returns a list of the results'''
    with pool_type(processes) as pool:
        results = pool.starmap(fn, args)
    # close the pool and wait for results to return
    return results


def safe_multithread(fn, args=[[]], processes=8):
    '''Guaranteed threadsafe version of multithread using ThreadPool'''
    return multithread(fn, args=args, pool_type=ThreadPool, processes=processes)


def multithread_failsafe(fn, args=[[]], pool_type=Pool,
                         processes=4):
    '''Aynchronous multithreading that does not break on individual errors.
    Instead, prints error and message, and the input is disregarded'''
    with pool_type(processes) as pool:
        threads = []
        for elem in args:
            threads.append(pool.apply_async(fn, elem))
        results = []
        for r in threads:
            try:
                results.append(r.get())
            except Exception as e:
                print(type(e), e)
    return results


def safe_multithread_failsafe(fn, args=[[]], processes=4):
    '''Threadsafe version of multithread_failsafe'''
    return multithread_failsafe(fn, args=args, pool_type=ThreadPool,
                                processes=processes)
