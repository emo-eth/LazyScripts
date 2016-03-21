from multiprocessing.pool import ThreadPool
import timeit


class jwmultithreaded(object):

    def __init__(self):
        self.cache_updated = False
        pass

    def multithread_impure(self, fn, args=[[]], pool_type=ThreadPool,
                           processes=4):
        '''multithreading helper function for impure functions.
        skips append so should be slightly quicker'''
        pool = pool_type(processes)
        thread_result = []
        for elem in args:
            thread_result.append(pool.apply_async(fn, elem))
        for r in thread_result:
            try:
                r.get()
            except Exception as e:
                print(type(e), e)
                self.cache_updated = False
                # don't writeout bad cache
        pool.close()

    def multithread(self, fn, args=[[]], pool_type=ThreadPool,
                    processes=4):
        '''Generic multithreading helper function'''
        pool = pool_type(processes)
        threads = []
        for elem in args:
            threads.append(pool.apply_async(fn, elem))
        results = []
        for r in threads:
            try:
                results.append(r.get())
            except Exception as e:
                print(type(e), e)
                self.cache_updated = False
        pool.close()
        return results


def multithread_impure(fn, args=[[]], pool_type=ThreadPool,
                       processes=4):
    '''multithreading helper function for impure functions.
    skips append so should be slightly quicker'''
    pool = pool_type(processes)
    thread_result = []
    for elem in args:
        thread_result.append(pool.apply_async(fn, elem))
    for r in thread_result:
        try:
            r.get()
        except Exception as e:
            print(type(e), e)
    pool.close()


def multithread(fn, args=[[]], pool_type=ThreadPool,
                processes=4):
    '''Generic multithreading helper function'''
    pool = pool_type(processes)
    threads = []
    for elem in args:
        threads.append(pool.apply_async(fn, elem))
    results = []
    for r in threads:
        try:
            results.append(r.get())
        except Exception as e:
            print(type(e), e)
    pool.close()
    return results


class test(jwmultithreaded):

    def __init__(self):
        self.imp = []
        self.args = [[x] for x in range(0, 100)]
        self.pure()
        self.impure()

    def pure(self):
        def wrap():
            self.multithread(self.square_impure, self.args)
        print(timeit.Timer(wrap).timeit(number=1500))

    def impure(self):
        def wrap():
            self.multithread_impure(self.square_impure, self.args)
        print(timeit.Timer(wrap).timeit(number=1500))

    def square_pure(self, x):
        return x * x

    def square_impure(self, x):
        self.imp.append(x * x)
