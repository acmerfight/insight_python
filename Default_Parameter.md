Python对于默认参数的处理往往会给新手造成困扰（但是通常只有一次）。

当你使用“可变”的对象作为函数中作为默认参数时会往往引起问题。这个参数可以在不创建新对象的情况下进行修改，例如 list dict。

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

原因很简单: 在每次函数调用的时候，函数一直再使用同一个对象。我们这么使用引起的变化，非常“sticky”。

#### 为什么会发生这种情况？
当且仅当默认参数所在的“def”语句执行的时候，默认参数才会进行计算。请看文档的描述

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
