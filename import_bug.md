

    
   奇怪的 dead lock
==========

在服务器上的程序遇到一个 `import` 卡死的情况，而且这个 bug 只能在服务器上重现，个人电脑上不会重现。去掉无用的部分，可以抽象出如下的代码

**bar.py**

    # coding=utf-8

    from threading import Thread

    class Bar(Thread):
        def run(self):
            u"知乎".encode("utf-8")
  
    bar = Bar()
    bar.start()
    bar.join()
**foo.py**
    
    import bar

执行 `python foo.py`，程序就卡死不动了。

要解决这个问题，首先必须要知道的是程序卡在哪里了，所以使用 [trace][1] 模块去看程序的执行流程。
执行 `python -m trace -t foo.py`，这是程序调用的最后的部分。

    __init__.py(93):     for modname in modnames:
    __init__.py(94):         if not modname or '.' in modname:
    __init__.py(96):         try:
    __init__.py(99):             mod = __import__('encodings.' + modname, fromlist=_import_tail,
    __init__.py(100):                              level=0)
    threading.py(237):         waiter = _allocate_lock()
    threading.py(238):         waiter.acquire()
    threading.py(239):         self.__waiters.append(waiter)
    threading.py(240):         saved_state = self._release_save()
     --- modulename: threading, funcname: _release_save
    threading.py(220):         self.__lock.release()           # No state to save
    threading.py(241):         try:    # restore state no matter what (e.g., KeyboardInterrupt)
    threading.py(242):             if timeout is None:
    threading.py(243):                 waiter.acquire()
    
我们很明显的看到了程序是卡在了**获得锁的时候**，但是我的程序里没有明确的加锁啊，为什么出现这种情况呢？通过调用记录向上追溯看到
`mod = __import__('encodings.' + modname, fromlist=_import_tail, level=0)`
是这一步引入了最后的锁，发现包含这行代码的文件是 `/usr/lib/python2.7/encodings/__init__.py`，大致猜出是执行`u"知乎".encode("utf-8")`卡死的。

现在再看 `__import__` 的实现，发现 `PyImport_ImportModuleLevel` 调用了 `_PyImport_AcquireLock`，当  `import_module_level` 成功后调用 `_PyImport_ReleaseLock`。

    PyObject *
    PyImport_ImportModuleLevel(char *name, PyObject *globals, PyObject *locals,
                             PyObject *fromlist, int level)
    {
        PyObject *result;
        _PyImport_AcquireLock();
        result = import_module_level(name, globals, locals, fromlist, level);
        if (_PyImport_ReleaseLock() < 0) {
            Py_XDECREF(result);
            PyErr_SetString(PyExc_RuntimeError,
                            "not holding the import lock");
            return NULL;
        }
        return result;
    }
    
再去继续看 [_PyImport_AcquireLock][2] 的代码可以明显的看到有一个 `import_lock` 存在。也就是 `import` 的时候会引入`import_lock`, 当我们 `import bar` 的时候，首先会获得 `import_lock`，但是当我们执行到 `mod = __import__('encodings.' + modname, fromlist=_import_tail, level=0)`的时候新创建的线程会再次去请求获得`import_lock`。在一把锁内部，再次请求获得这把锁造成了死锁，使程序直接卡住了。在服务器上把`u"知乎".encode("utf-8")`  换成 `import socket` 照样会卡在 `import_lock` 处。

通过分析，现在终于找出原因了。但是为什么只能在服务上重现呢？为什么本地的机器没有问题？

我把 `u"知乎".encode("utf-8")` 换成 `import socket` ，在本地执行也会卡在 `import_lock`。那为什么 `u"知乎".encode("utf-8")` 为啥在本地不卡呢。那就用 `ipdb` 看看`u"知乎".encode("utf-8")`在本地和服务器上的调用有啥不同吧。

     #coding=utf-8
      
     import ipdb
     ipdb.set_trace()
     u"知乎".encode("utf-8")
结果发现在本地根本就没有进入 `search_function`，程序执行完。而在服务器上直接进入了 `/usr/lib/python2.7/encodings/__init__.py` 文件，逐步的执行到 `__import__` 造成了死锁。为什么本地的机器上不用加载呢？

在本地的 [encodings/__init__.py][3] 文件里加上调试信息 `print encoding`，发现在本地直接输入 `python` 启动命令行，直接就打印出了 `utf-8`，而在服务器上是 `ascii`。原来不同的机器上加载的默认编码不一样。通过 `locale.getdefaultlocale` 也发现默认的编码服务器默认的编码是 `ascii`，本地是 `utf-8`。

终于知道了原来根据环境不同，默认加载的编码是不一样的，加载了的编码会有 cache 就不用执行到 `__import__ `，没有加载过的编码就会执行。我又在自己的服务器上把 `encode("utf-8")` 改成`encode("utf8")`，发现本地的程序也卡在了 `__import__` 的地方。

至此这个 bug，终于搞清楚了，真是艰难。简单总结下

**一般在最外层只写函数，类，变量定义代码。其它有副作用的代码都放到函数里，尤其不能在最外层写 Thread.join 这种会 block 住整个程序运行的代码。`import` 完之后在显式调用函数来执行这些代码。原则是使 `import` 尽量不带有副作用。**

这个问题得以解决，绝大部分的功劳属于[安江泽][4]。同时感谢Leo Jay 的指正。



  [1]: https://docs.python.org/2/library/trace.html
  [2]: http://hg.python.org/cpython/file/7caf7401aece/Python/import.c#l292
  [3]: http://hg.python.org/cpython/file/7caf7401aece/Lib/encodings/__init__.py#l72
  [4]: http://www.zhihu.com/people/gnap
