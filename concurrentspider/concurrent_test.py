# 多线程
# Python中的GIL问题:
# GIL的全称: Global Interpreter Lock 全局解释器锁, 来源是python设计之初的考虑，为了数据安全所做的决定。
# 每个CPU在同一时间只能执行一个线程

# 在Python多线程下，每个线程的执行方式：
# 1.获取GIL
# 2.执行代码直到sleep或者是python虚拟机将其挂起。
# 3.释放GIL

# GIL的释放:
# 1. 时间片释放, 指定时间释放.
# 2. 遇到io释放.

# 那么是不是python的多线程就完全没用了呢？
# 在这里我们进行分类讨论：

# 1、CPU密集型代码(各种循环处理、计数等等)，
# 在这种情况下，ticks计数很快就会达到阈值，然后触发GIL的释放与再竞争（多个线程来回切换当然是需要消耗资源的），
# 所以python下的多线程对CPU密集型代码并不友好。

#2、IO密集型代码(文件处理、网络爬虫等)，多线程能够有效提升效率(单线程下有IO操作会进行IO等待，造成不必要的时间浪费，
# 而开启多线程能在线程A等待时，自动切换到线程B，可以不浪费CPU的资源，从而能提升程序执行效率)。所以python的多线程对IO密集型代码比较友好。


# Python的threading模块里的消息通信机制主要有:
# 1. Event
# 2. Condition
# 3. Queue
# 使用最多的是Queue, 是线程安全的, 当我们对它进行写入和提取的操作不会被中断, 不需要额外加锁


#One Producer and One Consumer, each on a thread
#Demonstrates queue and lock
import random
import threading
import multiprocessing
from threading import Thread
from queue import Queue

finished = False


def display(msg):
    threadname = threading.current_thread().name
    processname = multiprocessing.current_process().name
    print('processname: {} \ threadname: {}: msg: {}'.format(processname, threadname, msg))


#Producer
def create_work(queue, max):
    for x in range(max):
        v = random.randint(1,100)
        queue.put(v)
        display(f'Producing {x}: {v}')

    global finished
    finished = True
    display('PRODUCE FINISHED')


#Consumer
def perform_work(work):
    counter = 0
    while True:
        if not work.empty():
            v = work.get()
            display(f'Consuming {counter} : {v}')
            counter += 1
        else:
            if finished == True:
                break

    display('CONSUME FINISHED')


def main():
    max = 50;
    work = Queue()

    producer = Thread(target=create_work, args=[work, max], daemon=True)
    consumer = Thread(target=perform_work, args=[work], daemon=True)

    producer.start()
    consumer.start()

    producer.join()
    display('Producer has finished')

    consumer.join()
    display('Consumer has finished')

    display('Main is finished')



if __name__ == '__main__':
    main()








