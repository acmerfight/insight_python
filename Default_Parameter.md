Python对于函数中默认参数的处理往往会给新手造成困扰（但是通常只有一次）。

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

像你所看到的那样，list变得越来越长。如果你仔细地查看这个list。你会发现list一直是同一个对象。

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

在老代码中，written before “object” was introduced，你有时会看到

'sentinel = ['placeholder']'

used to create a non-false object with a unique identity; [] creates a new list every time it is evaluated.
#### 正确地使用可变参数
最后需要注意的是一些高深的Python代码经常会利用这个机制的优势；举个例子，如果在一个循环里创建一些UI上的按钮，你可能会尝试这样去做：

    for i in range(10):
        def callback():
            print "clicked button", i
        UI.Button("button %s" % i, callback)

但是你却发现`callback`打印出相同的数字（在这个情况下很可能是9）。The reason for this is that Python’s nested scopes bind to variables, not object values, so all callback instances will see the current (=last) value of the “i” variable. To fix this, use explicit binding:

    for i in range(10):
        def callback(i=i):
            print "clicked button", i
        UI.Button("button %s" % i, callback)

The “i=i” part binds the parameter “i” (a local variable) to the current value of the outer variable “i”.

另外的两个用途local caches/memoization
        
    def calculate(a, b, c, memo={}):
    try:
        value = memo[a, b, c] # return already calculated value
    except KeyError:
        value = heavy_calculation(a, b, c)
        memo[a, b, c] = value # update the memo dictionary
    return value

（对一些递归算法非常好用）

对高度优化的代码而言， local rebinding of global names:

    import math

    def this_one_must_be_fast(x, sin=math.sin, cos=math.cos):
        ...

#### 这是如何工作的？
当Python执行一条`def`语句时， it takes some ready-made pieces (including the compiled code for the function body and the current namespace)，创建了一个新的函数对象。同时，计算了函数的默认参数值。

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

然而我推荐你平时这么使用。

另一个重置默认参数的方法是重新执行相同的`def`语句，Python will then create a new binding to the code object, 计算默认参数，and assign the function object to the same variable as before. But again, only do that if you know exactly what you’re doing.

And yes, if you happen to have the pieces but not the function, you can use the function class in the new module to create your own function object.
