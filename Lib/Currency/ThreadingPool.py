from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import time

"""
IO 密集型任务选择multiprocessing.dummy，CPU 密集型任务选择multiprocessing
"""


class ThreadingPool:
    def __init__(self, num):
        self.num = num
        pass

    def multi_process(self, fun, lists):
        pool = Pool(self.num)
        pool.map(fun, lists)
        pool.close()
        pool.join()

    def multi_thread(self, fun, lists):
        pool = ThreadPool(self.num)
        pool.map(fun, lists)
        pool.close()
        pool.join()


if __name__ == "__main__":
    def add(a):
        print(a)
        time.sleep(1)
        return


    attrs = [1, 2, 3]
    threadingpool = ThreadingPool(4)
    threadingpool.multi_process(add, attrs)


    # def openfile(a):
    #     with open(a, 'w') as f:
    #         f.write('a')
    #
    # attrs = ['a.txt', 'b.txt', 'c.txt']
    #
    # threadingpool = ThreadingPool(openfile, attrs)
    # threadingpool.multi_process()
