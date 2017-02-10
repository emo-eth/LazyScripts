import unittest
import types
from utils import *
from LazyScripts.LazyMultithread import *


class multithreadedTest(unittest.TestCase):

    def test_multithread(self):
        results = multithread(multithread_test, [[1, 2, 3], [4, 5, 6]])
        self.assertTrue(results)
        results = multithread(multithread_test, [[1, 2, 3], [4, 5, 6]],
                              chunksize=2, maxtasksperchild=2)
        self.assertTrue(results)

    def test_safe_multithread(self):
        results = safe_multithread(multithread_test, [[1, 2, 3], [4, 5, 6]])
        self.assertTrue(results)
        results = safe_multithread(multithread_test, [[1, 2, 3], [4, 5, 6]],
                                   chunksize=2)
        self.assertTrue(results)

    def test_multithread_failsafe(self):
        results = multithread_failsafe(multithread_test,
                                       [[1, 2, 3], [4, 5, 0]], verbose=True)
        print(type(results), results)
        results = list(results)
        self.assertTrue(results)
        self.assertTrue(len(results) == 1)
        results = multithread_failsafe(multithread_test,
                                       [[1, 2, 3], [4, 5, 0]], chunksize=2,
                                       verbose=False)
        results = list(results)
        self.assertTrue(results)
        self.assertTrue(len(results) == 1)

    def test_safe_multithread_failsafe(self):
        results = safe_multithread_failsafe(multithread_test,
                                            [[1, 2, 3], [4, 5, 0]],
                                            verbose=False)
        self.assertTrue(isinstance(results, types.GeneratorType))
        results = list(results)
        self.assertTrue(results)
        self.assertTrue(len(results) == 1)
        results = safe_multithread_failsafe(multithread_test,
                                            [[1, 2, 3], [4, 5, 0]],
                                            chunksize=2, verbose=False)
        self.assertTrue(results)
        results = list(results)
        self.assertTrue(len(results) == 1)

    def test_assert_yield(self):
        # self.assertTrue(False)
        results = multithread_failsafe(multithread_test,
                                       [[4, 5, 0], [1, 2, 3]], verbose=False)
        print(type(results), results)
        results = list(results)
        self.assertTrue(results)
        self.assertTrue(len(results) == 1)
        print(results)

if __name__ == '__main__':
    unittest.main()
