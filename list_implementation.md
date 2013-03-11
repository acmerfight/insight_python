##Python中list 的实现  
这篇文章介绍了Python中list是如何实现的。  
在Python中list特别有用。让我们来看下list的内部是如何实现的。  
来看下面简单的程序，在list中添加一些整数并将他们打印出来。  

    >>> L = []
    >>> L.append(1)
    >>> L.append(2)
    >>> L.append(3)
    >>> L
    [1, 2, 3]
    >>> for e in L:
    ...   print e
    ... 
    1
    2
    3
正如你所看到的，list是可以迭代的。  

###List对象的C结构  
Python中一个list对象是用下边的C的结构来表现的。ob_item是用来保存元素的指针数组，allocated是在内存中预先分配的总容量

    typedef struct {
        PyObject_VAR_HEAD
        PyObject **ob_item;
        Py_ssize_t allocated;
    } PyListObject;
