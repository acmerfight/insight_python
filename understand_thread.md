我们将会看到一些在Python中使用线程的实例和如何避免线程之间的竞争。

你应当将下边的例子运行多次，以便可以注意到线程是不可预测的和线程每次运行出的不同结果。

声明：从这里开始忘掉你听到过的关于GIL的东西，因为GIL不会影响到我想要展示的东西。

#### 示例1:
我们将要请求五个不同的url：

##### 单线程

    import time
    import urllib2

    def get_responses():
        urls = [
            'http://www.google.com',
            'http://www.amazon.com',
            'http://www.ebay.com',
            'http://www.alibaba.com',
            'http://www.reddit.com'
        ]
        start = time.time()
        for url in urls:
            print url
            resp = urllib2.urlopen(url)
            print resp.getcode()
        print "Elapsed time: %s" % (time.time()-start)

    get_responses()

输出是：

    http://www.google.com 200
    http://www.amazon.com 200
    http://www.ebay.com 200
    http://www.alibaba.com 200
    http://www.reddit.com 200
    Elapsed time: 3.0814409256

解释：  
1.  url顺序的被请求  
2.  除非cpu从一个url获得了回应，否则不会去请求下一个url  
3.  网络请求会花费较长的时间，所以cpu在等待网络请求的返回时间内一直处于闲置状态。  

##### 多线程

    import urllib2
    import time
    from threading import Thread

    class GetUrlThread(Thread):
        def __init__(self, url):
            self.url = url 
            super(GetUrlThread, self).__init__()

        def run(self):
            resp = urllib2.urlopen(self.url)
            print self.url, resp.getcode()

    def get_responses():
        urls = [
            'http://www.google.com', 
            'http://www.amazon.com', 
            'http://www.ebay.com', 
            'http://www.alibaba.com', 
            'http://www.reddit.com'
        ]
        start = time.time()
        threads = []
        for url in urls:
            t = GetUrlThread(url)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        print "Elapsed time: %s" % (time.time()-start)

    get_responses()

输出:  
    http://www.reddit.com 200
    http://www.google.com 200
    http://www.amazon.com 200
    http://www.alibaba.com 200
    http://www.ebay.com 200
    Elapsed time: 0.689890861511

解释：
*   意识到了程序在执行时间上的提升
*   我们写了一个多线程程序来减少cpu的等待时间，当我们在等待一个线程内的网络请求返回时，这时cpu可以切换到其他线程去进行其他线程内的网络请求。
*   我们期望一个线程处理一个url，所以实例化线程类的时候我们传了一个url。
*   线程运行意味着执行类里的`run()`方法。
*   无论如何我们想每个线程必须执行`run()`。
*   为每个url创建一个线程并且调用`start()`方法，这告诉了cpu可以执行线程中的`run()`方法了。
*   我们希望所有的线程执行完毕的时候再计算花费的时间，所以调用了`join()`方法。
*   `join()`可以通知主线程等待这个线程结束后，才可以执行下一条指令。
*   每个线程我们都调用了join方法，所以我们是在所有线程执行完毕后计算的运行时间。

关于线程：  
*   cpu可能不会在调用`start()`后马上执行`run()`方法。
*   你不能确定`run()`在不同线程建间的执行顺序。
*   对于单独的一个线程，可以保证`run()`方法里的语句是按照顺序执行的。
*   这就是因为线程内的url会首先被请求，然后打印出返回的结果。

#### 实例2

我们将会用一个程序演示一下多线程间的资源竞争，并修复这个问题。  

    from threading import Thread


    #define a global variable
    some_var = 0 

    class IncrementThread(Thread):
        def run(self):
            #we want to read a global variable
            #and then increment it
            global some_var
            read_value = some_var
            print "some_var in %s is %d" % (self.name, read_value)
            some_var = read_value + 1 
            print "some_var in %s after increment is %d" % (self.name, some_var)

    def use_increment_thread():
        threads = []
        for i in range(50):
            t = IncrementThread()
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        print "After 50 modifications, some_var should have become 50"
        print "After 50 modifications, some_var is %d" % (some_var,)

    use_increment_thread()

多次运行这个程序，你会看到多种不同的结果。  
解释：
*   有一个全局变量，所有的线程都想修改它。
*   所有的线程应该在这个全局变量上加 1 。
*   有50个线程，最后这个数值应该变成50，但是它却没有。

为什么没有达到50？  
*   在`some_var`是`15`的时候，线程`t1`读取了`some_var`，这个时刻cpu将控制权给了另一个线程`t2`。
*   `t2`线程读到的`some_var`也是`15`
*   `t1`和`t2`都把`some_var`加到`16`
*   当时我们期望的是`t1` `t2`两个线程使`some_var + 2`变成`17`
*   在这里就有了资源竞争。
*   相同的情况也可能发生在其它的线程间，所以出现了最后的结果小于`50`的情况。

解决竞争资源

    from threading import Lock, Thread
    lock = Lock()
    some_var = 0 


    class IncrementThread(Thread):
        def run(self):
            #we want to read a global variable
            #and then increment it
            global some_var
            lock.acquire()
            read_value = some_var
            print "some_var in %s is %d" % (self.name, read_value)
            some_var = read_value + 1 
            print "some_var in %s after increment is %d" % (self.name, some_var)
            lock.release()

    def use_increment_thread():
        threads = []
        for i in range(50):
            t = IncrementThread()
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        print "After 50 modifications, some_var should have become 50"
        print "After 50 modifications, some_var is %d" % (some_var,)

    use_increment_thread()


再次运行这个程序，达到了我们预期的结果。  
解释：  
*   Lock 用来防止竞争条件
*   如果在执行一些操作之前，线程`t1`获得了锁。其他的线程在`t1`释放Lock之前，不会执行相同的操作
*   我们想要确定的是一旦线程`t1`已经读取了`some_var`，直到`t1`完成了修改`some_var`，其他的线程才可以读取`some_var`
*   这样读取和修改`some_var`都成了逻辑上的原子操作。

#### 实例3

    from threading import Thread
    import time

    class CreateListThread(Thread):
        def run(self):
            self.entries = []
            for i in range(10):
                time.sleep(1)
                self.entries.append(i)
            print self.entries

    def use_create_list_thread():
        for i in range(3):
            t = CreateListThread()
            t.start()

    use_create_list_thread()

    from threading import Thread, Lock
    import time

    lock = Lock()

    class CreateListThread(Thread):
        def run(self):
            self.entries = []
            for i in range(10):
                time.sleep(1)
                self.entries.append(i)
            lock.acquire()
            print self.entries
            lock.release()

    def use_create_list_thread():
        for i in range(3):
            t = CreateListThread()
            t.start()

    use_create_list_thread()

