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
Python中一个list对象是用下边的C的结构来表现的。ob_item是用来保存list元素的指针数组，allocated是在内存中预先分配的总容量

    typedef struct {
        PyObject_VAR_HEAD
        PyObject **ob_item;
        Py_ssize_t allocated;
    } PyListObject;

###List的初始化
让我们来看下当初始化一个空list的时候发生了什么 L = []
    
    arguments: size of the list = 0
    returns: list object = []
    PyListNew:
        nbytes = size * size of global Python object = 0
        allocate new list object
        allocate list of pointers (ob_item) of size nbytes = 0
        clear ob_item
        set list's allocated var to 0 = 0 slots
        return list object 

非常重要的是知道allocated的大小和list大小之间的关系，list的大小和len(L)是一样的，而allocated的大小是在内存中已经申请空间大小。通常你会看到allocated的值要比list的值要大。这是为了避免每次有新元素加入list时都要调用realloc进行内存分配。接下来我们会看到更多关于这些的内容。
