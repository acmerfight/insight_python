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
###Append
我们在list中追加一个整数:L.append(1)。发生了什么？调用了内部的C函数app1()

    arguments: list object, new element
    returns: 0 if OK, -1 if not
    app1:
        n = size of list
        call list_resize() to resize the list to size n+1 = 0 + 1 = 1
        list[n] = list[0] = new element
        return 0

来让我们看下list_resize()。list_resize()会申请多余的空间以避免调用多次list_resize()函数，list增长的模型是:0, 4, 8, 16, 25, 35, 46, 58, 72, 88, …

    arguments: list object, new size
    returns: 0 if OK, -1 if not
    list_resize:
        new_allocated = (newsize >> 3) + (newsize < 9 ? 3 : 6) = 3
        new_allocated += newsize = 3 + 1 = 4
        resize ob_item (list of pointers) to size new_allocated
        return 0

开辟了四个内存空间来存放list中的元素，存放的第一个元素是1。你可以从下图中看到L[0]指向了我们刚刚加进去的元素。虚线的框代表了申请了但是还没有使用的内存空间  
![](https://raw.github.com/acmerfight/insight_python/master/list.png)  
我们继续加入一个元素：L.append(2)。调用list_resize,伴随着n+1=2。但是因为allocated size（译者注：已经申请的空间大小）是4。所以没有必要去申请新的内存空间。相同的事情发生在再次在list中添加两个元素的时候：L.append(3),L.append(4)。下图展示了到目前为止我们做了什么。
