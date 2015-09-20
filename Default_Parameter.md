#### 文章的主题
不要使用可变对象作为函数的默认参数例如 list，dict，因为`def`是一个可执行语句，只有`def`执行的时候才会计算默认默认参数的值，所以使用默认参数会造成函数执行的时候一直在使用同一个对象，引起bug。

#### 基本原理
在 Python 源码中,我们使用`def`来定义函数或者方法。在其他语言中,类似的东西往往只是一一个语法声明关键字,但`def`却是一个可执行的指令。Python 代码执行的时候先会使用 compile 将其编译成 PyCodeObject.

PyCodeObject 本质上依然是一种静态源代码,只不过以字节码方式存储,因为它面向虚拟机。因此 Code 关注的是如何执行这些字节码,比如栈空间大小,各种常量变量符号列表,以及字节码与源码行号的对应关系等等。

PyFunctionObject 是运行期产生的。它提供一个动态环境,让 PyCodeObject 与运行环境关联起来。同时为函数调用提供一系列的上下文属性,诸如所在模块、全局名字空间、参数默认值等等。这是`def`语句执行的时候干的活。

PyFunctionObject 让函数面向逻辑,而不仅仅是虚拟机。PyFunctionObject 和 PyCodeObject 组合起来才是一个完整的函数。

下文翻译了一篇文章，有一些很好的例子。但是由于水平有限，有些不会翻译或者有些翻译有误，敬请谅解。如果有任何问题请发邮件到 acmerfight圈gmail.com,感激不尽

主要参考资料 书籍：《深入Python编程》 大牛：shell 和 Topsky

[原文链接](http://effbot.org/zone/default-values.htm)

Python 对于函数中默认参数的处理往往会给新手造成困扰（但是通常只有一次）。

当你使用“可变”的对象作为函数中作为默认参数时会往往引起问题。因为在这种情况下参数可以在不创建新对象的情况下进行修改，例如 list dict。

    >>> def function(data=[]):
    ...     data.append(1)
    ...     return data
    ...
    >>> function()
    [1]
    >>> function()
    [1, 1]
    >>> function()
    [1, 1, 1]

像你所看到的那样，list 变得越来越长。如果你仔细地查看这个 list。你会发现 list 一直是同一个对象。

    >>> id(function())
    12516768
    >>> id(function())
    12516768
    >>> id(function())
    12516768

原因很简单: 在每次函数调用的时候，函数一直再使用同一个list对象。这么使用引起的变化，非常“sticky”。

#### 为什么会发生这种情况？
**当且仅当**默认参数所在的“def”语句执行的时候，默认参数才会进行计算。请看文档描述

[http://docs.python.org/ref/function.html](http://docs.python.org/ref/function.html)

的相关部分。

"def"是Python中的可执行语句，默认参数在"def"的语句环境里被计算。如果你执行了"def"语句多次，每次它都将会创建一个新的函数对象。接下来我们将看到例子。
#### 用什么来代替？
像其他人所提到的那样，用一个占位符来替代可以修改的默认值。`None` 

    def myfunc(value=None):
        if value is None:
            value = []
        # modify value here

如果你想要处理任意类型的对象，可以使用sentinel

    sentinel = object()

    def myfunc(value=sentinel):
        if value is sentinel:
            value = expression
        # use/modify value here

在比较老的代码中，written before “object” was introduced，你有时会看到

    sentinel = ['placeholder']

    译者注：太水，真的不知道怎么翻译了。我说下我的理解 有时逻辑上可能需要传递一个None,而你的默认值可能又不是None,而且还刚好是个列表,列表不
    可以写在默认值位置,所以你需要占位符,但是用None，你又不知道是不是调用者传递过来的那个
#### 正确地使用可变参数
最后需要注意的是一些高深的Python代码经常会利用这个机制的优势；举个例子，如果在一个循环里创建一些UI上的按钮，你可能会尝试这样去做：

    for i in range(10):
        def callback():
            print "clicked button", i
        UI.Button("button %s" % i, callback)

但是你却发现`callback`打印出相同的数字（在这个情况下很可能是9）。原因是Python的嵌套作用域只是绑定变量，而不是绑定数值的，所以`callback`只看到了变量`i`绑定的最后一个数值。为了避免这种情况，使用显示绑定。

    for i in range(10):
        def callback(i=i):
            print "clicked button", i
        UI.Button("button %s" % i, callback)

`i=i`把callback的参数`i`(一个局部变量)绑定到了当前外部的`i`变量的数值上。(译者注：如果不理解这个例子，请看[http://stackoverflow.com/questions/233673/lexical-closures-in-python](http://stackoverflow.com/questions/233673/lexical-closures-in-python))

另外的两个用途local caches/memoization
        
    def calculate(a, b, c, memo={}):
        try:
            value = memo[a, b, c] # return already calculated value
        except KeyError:
            value = heavy_calculation(a, b, c)
            memo[a, b, c] = value # update the memo dictionary
        return value

（对一些递归算法非常好用）

对高度优化的代码而言， 会使用局部变量绑全局的变量:

    import math

    def this_one_must_be_fast(x, sin=math.sin, cos=math.cos):
        ...

#### 这是如何工作的？
当Python执行一条`def`语句时， 它会使用已经准备好的东西（包括函数的代码对象和函数的上下文属性），创建了一个新的函数对象。同时，计算了函数的默认参数值。

不同的组件像函数对象的属性一样可以使用。上文用到的'function'

    >>> function.func_name
    'function'
    >>> function.func_code
    <code object function at 00BEC770, file "<stdin>", line 1>
    >>> function.func_defaults
    ([1, 1, 1],)
    >>> function.func_globals
    {'function': <function function at 0x00BF1C30>,
    '__builtins__': <module '__builtin__' (built-in)>,
    '__name__': '__main__', '__doc__': None}

这样你可以访问默认参数，你甚至可以修改它。

    >>> function.func_defaults[0][:] = []
    >>> function()
    [1]
    >>> function.func_defaults
    ([1],)

然而我不推荐你平时这么使用。

另一个重置默认参数的方法是重新执行相同的`def`语句，Python将会和代码对象创建一个新的函数对象，并计算默认参数，并且把新创建的函数对象赋值给了和上次相同的变量。但是再次强调，只有你清晰地知道在做什么的情况下你才能这么做。

And yes, if you happen to have the pieces but not the function, you can use the function class in the new module to create your own function object.
