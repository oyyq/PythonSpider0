#线程池

from concurrent.futures import ThreadPoolExecutor,wait, ALL_COMPLETED, FIRST_COMPLETED, as_completed
import time


def sleep_task(sleep_time):
    print("sleep {} s".format(sleep_time))
    time.sleep(sleep_time)


executor = ThreadPoolExecutor(max_workers=2)
executor.submit(sleep_task, 2)
task1 = executor.submit(sleep_task, 3)    #Future in _base.py
task1.cancel()                            #取消一个Future, 若Future is running or already be completed, 则无法取消
task1.done()                              #task是否已经完成

wait([task1], return_when=ALL_COMPLETED)  #阻塞主线程, 等待所有Future执行完成
print("main end")

all_task = [task1]
for task in as_completed(all_task):
    print(task.result())                #当任务执行完毕, 拿到返回值
