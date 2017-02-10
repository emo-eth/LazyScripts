from multiprocessing.pool import Pool, ThreadPool
from multiprocessing import cpu_count
import traceback
# for reference:
# from multiprocessing import Manager, Lock

_cpus = cpu_count()


def multithread(fn, args=[[]], pool_type=Pool,
                processes=_cpus, maxtasksperchild=1,
                chunksize=1):
    '''Multithread method using a Pool. Not inherently threadsafe.
    For threadsafe operations, use Managers or Locks.
    Args must be wrapped in their own iterator, as starmap is used for
    multiple arguments.
    Returns an iterator of the results'''

    def helper(pool):
        return pool.starmap(fn, args, chunksize=chunksize)

    # ThreadPools do not take a maxtasksperchild argument,
    # so we need to conditionally construct a pool

    if type(pool_type) is Pool:
        with pool_type(processes, maxtasksperchild=maxtasksperchild) as pool:
            results = helper(pool)
    else:
        with pool_type(processes) as pool:
            results = helper(pool)
    return results


def safe_multithread(fn, args=[[]], processes=_cpus, chunksize=1):
    '''Guaranteed threadsafe version of multithread using ThreadPool.
    Allows child threads. Limited by interpreter lock.'''
    return multithread(fn, args=args, pool_type=ThreadPool,
                       processes=processes, chunksize=chunksize)


def multithread_failsafe(fn, args=[[]], pool_type=Pool,
                         processes=_cpus, maxtasksperchild=1, chunksize=1,
                         verbose=True):
    '''Aynchronous multithreading that does not break on individual errors.
    Instead, prints error and message, and the input is disregarded

    Unfortunately, due to context-management restrictions, (as far as I can
    tell) both generators are needed even though the only difference is the
    maxtasksperchild arg'''

    '''Generators that yield next completed task. While execution of individual
    tasks is asynchronous, iterating through the results is not'''

    def process_generator(pool_type):
        with pool_type(processes, maxtasksperchild=maxtasksperchild) as pool:
            result_objs = (pool.apply_async(fn, arg) for arg in args)
            for r in result_objs:
                try:
                    yield r.get()
                except GeneratorExit as g:
                    raise g
                except:
                    if verbose:
                        print('######BEGIN TRACEBACK######')
                        traceback.print_exc()
                        print('######END TRACEBACK######')
                        print()
                    continue

    def thread_generator(pool_type):
        with pool_type(processes) as pool:
            result_objs = (pool.apply_async(fn, arg) for arg in args)
            for r in result_objs:
                try:
                    yield r.get()
                except GeneratorExit as g:
                    raise g
                except:
                    if verbose:
                        print('######BEGIN TRACEBACK######')
                        traceback.print_exc()
                        print('######END TRACEBACK######')
                        print()
                    continue

    # ThreadPools do not take a maxtasksperchild argument,
    # so we need to conditionally construct a generator

    if issubclass(pool_type, ThreadPool):
        return thread_generator(pool_type)
    else:
        return process_generator(pool_type)


def safe_multithread_failsafe(fn, args=[[]], processes=_cpus, chunksize=1,
                              verbose=True):
    '''Threadsafe version of multithread_failsafe.
    Allows child threads. Limited by interpreter lock.'''

    return multithread_failsafe(fn, args=args, pool_type=ThreadPool,
                                processes=processes, verbose=verbose)
