Python的self参数使一些人特别恼怒。举例来说,你必须在每个类的方法里显示地定义它(staticmethod除外)。它然后粗鲁地注入到了不想要他的地方。
    
    class Foo(object):
        x = 9
        def __init__(self, x):
            self.x = x
 
        def bar(self, y): 
            return self.x + y

如果你来自 C++, Java 或者其它相似的背景。self在`__init__`和`bar`中好像非常多余。Python总是吹嘘能写出简单和整洁的代码，但是看看它又带来了什么呢？
#### Scope Happens
Scope在Python中非常简洁。在Python中任何东西都是对象，几乎所有的东西都被定义在了对象这个级别。写一个module？

    # test.py
    def say_hi():
        print 'Hi!'

你创建了一个带有`say_hi`属性的module对象，

定义一个新的类？

    class Foo(object):
        x = 9
        def __init__(self, x):
            self.x = x
     
        def bar(self, y):
            return self.x + y

你创建了带有`x` `__init__` `bar`属性的一个类对象

实例化Foo？

    foo = Foo(5)

你创建了一个带有`x` `__init__` `bar`属性的Foo对象，请记住这三个属性在`Foo`和`foo`中是不一样的。接下来我们就将会知道其中的原因。
####Context is Everything
让我们来解析一下Foo：

    def bar(self,y):
        return self.x + y
     
    class Foo(object):
        x = 9
        def __init__(self,x):
            self.x = x
        bar = bar

先不要理 `bar` 的第一个参数 `self`。如果我们把 `bar` 只看成一个函数，下面发生情况就看起来非常合理。

    foo = Foo(5)
     
    print bar(foo, 4) == 9
    print bar(Foo, 0) == 9

似乎同样的事情看起来也能发生在 `Foo.bar` 上。

    print Foo.bar(foo, 4) == 9
    print Foo.bar(Foo, 0) == 9

但是第一行结果是 `True`。第二行出现了错误`TypeError: unbound method bar() must be called with Foo instance as first argument (got type instance instead).`

实例化`Foo`通过隐藏`self`参数更进一步的修改了`bar`。

    print foo.bar(foo, 4) == 9
    print foo.bar(foo, 0) == 9

两行都出现了错误`TypeError: bar() takes exactly 2 arguments (3 given)`。如果你曾经想知道为什么程序传了三个参数而不是两个，现在你将得到答案。
####Binding Self
如果你来检查这三个bar的类型，你将会看到他们是不一样的。

    print type(bar)
    # <type 'function'>
    print type(Foo.bar)
    # <type 'instancemethod'>
    print type(foo.bar)
    # <type 'instancemethod'>

在类里直接加入任何函数，加入的函数将会被包装成instancemethod对象，instancemethod像胶水一样把类，实例（如果有的话），和原始的函数粘在在了一起。

    print Foo.bar.im_class == Foo
    print Foo.bar.im_func == bar
    print Foo.bar.im_self == None
    print foo.bar.im_class == Foo
    print foo.bar.im_func == bar
    print foo.bar.im_self == foo

用Python代码可以直接的创建的一个简化的instancemethod。

class myinstancemethod(object):
    def __init__(self, func, cls, instance=None):
        self.im_func = func
        self.im_class = cls
        self.im_self = instance
 
    def __call__(_self, *args, **kwargs):
        args = list(args)
        if _self.im_self is not None:
            args.insert(0, _self.im_self)
             
        if len(args) == 0:
            raise TypeError("unbound method bar() must be called with Foo instance as first argument (got nothing instead)")
        elif not isinstance(args[0], _self.im_class):
            raise TypeError("unbound method bar() must be called with Foo instance as first argument (got %s instead)" % type(args[0]).__name__)
        else:
            return _self.im_func(*args, **kwargs)

myinstancemethod模拟真实的instancemethod非常准确。myinstancemethod与上文的例子中的`Foo.bar` `foo.bar`表现出相同的行为 ，plus it handles very well a few edge cases of class and instance method calling.

    my_unbound(self=foo,y=4)
    # TypeError: bar() got multiple values for keyword argument 'self'
    Foo.bar(self=foo,y=4)
    # TypeError: bar() got multiple values for keyword argument 'self'
     
    my_bound(self=foo,y=4)
    # TypeError: unbound method bar() must be called with Foo instance as first argument (got nothing instead)
    foo.bar(self=foo,y=4)
    # TypeError: unbound method bar() must be called with Foo instance as first argument (got nothing instead)

这就是为什么你可以传递引用给bar来替代传递foo并且调用foo.bar

####Closing
foo跟Foo完全不一样，每个在Python中的变量引用的是一个内存中的对象-对象也没什么不同。`Foo.x` `Foo.__init__` `Foo.bar`指向的内存位置跟`foo.x` 'foo.__init__' 'foo.bar'是不同的。

    print Foo.x is not foo.x
    print Foo.__init__ is not foo.__init__
    print Foo.bar is not foo.bar

foo and Foo are separate entities that happen to reference each other, in all the right places.
