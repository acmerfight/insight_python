我们将会看到一些在Python中使用线程的实例和如何避免线程之间的竞争。

你应当将下边的例子运行多次，以便可以注意到线程是不可预测的和线程每次运行出的不同结果。

声明：从这里开始忘掉你听到的关于GIL的消息，因为GIL不会影响到我想要展示的东西。

#### 示例1:
我们将要请求五个不同的url：

单线程的方法：

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
所有的url顺序的被请求  
除非cpu从一个url获得了回应，否则程序不会去请求下一个url  
网络操作会花费较长的时间，所以cpu在请求等待
