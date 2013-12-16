### Python中的method

#### 什么是method？
function就是可以通过名字可以调用的一段代码,我们可以传参数进去，得到返回值。所有的参数都是明确的传递过去的。  
method是function与对象的结合。我们调用一个方法的时候，有些参数是隐含的传递过去的。下文会详细介绍。
#### instance method

    In [5]: class Human(object):
       ...:     def __init__(self, weight):
       ...:         self.weight = weight
       ...:     def get_weight(self):
       ...:         return self.weight
       ...:     

    In [6]: Human.get_weight
    Out[6]: <unbound method Human.get_weight>

这告诉我们`get_weight`是一个没有被绑定方法，什么叫做未绑定呢？继续看下去。

    In [7]: Human.get_weight()
    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)
    /home/yao/learn/insight_python/<ipython-input-7-a2b2c5cd2f8d> in <module>()
    ----> 1 Human.get_weight()

    TypeError: unbound method get_weight() must be called with Human instance as first argument (got nothing instead)

未绑定的方法必须使用一个`Human`实例作为第一个参数来调用啊。那我们来试试

    In [10]: Human.get_weight(Human(45))
    Out[10]: 45

果然成功了，但是一般情况下我们习惯这么使用。

    In [11]: person = Human(45)

    In [12]: person.get_weight()
    Out[12]: 45

这两种方式的结果一模一样。我们看下官方文档是怎么解释这种现象的。

    When an instance attribute is referenced that isn’t a data attribute, its class is searched. 
    If the name denotes a valid class attribute that is a function object, a method object is 
    created by packing (pointers to) the instance object and the function object just found together
    in an abstract object: this is the method object. When the method object is called with an 
    argument list, a new argument list is constructed from the instance object and the argument list, 
    and the function object is called with this new argument list.

原来我们常用的调用方法(`person.get_weight()`)是把调用的实例隐藏的作为一个参数`self`传递过去了, `self` 只是一个普通的参数名称,不是关键字。

    In [13]: person.get_weight
    Out[13]: <bound method Human.get_weight of <__main__.Human object at 0x8e13bec>>

    In [14]: person
    Out[14]: <__main__.Human at 0x8e13bec>

我们看到`get_weight`被绑定在了 `person` 这个实例对象上。  
总结下  

1.  `instance method` 就是实例对象与函数的结合。  
2.  使用类调用，第一个参数明确的传递过去一个实例。  
3.  使用实例调用，调用的实例被作为第一个参数被隐含的传递过去。

#### classmethod

    In [1]: class Human(object):
       ...:     weight = 12
       ...:     @classmethod
       ...:     def get_weight(cls):
       ...:         return cls.weight

    In [2]: Human.get_weight
    Out[2]: <bound method type.get_weight of <class '__main__.Human'>>

我们看到`get_weight`是一个绑定在 `Human` 这个类上的method。调用下看看

    In [3]: Human.get_weight()
    Out[3]: 12
    In [4]: Human().get_weight()
    Out[4]: 12

类和类的实例都能调用 `get_weight` 而且调用结果完全一样。  
我们看到 `weight` 是属于 `Human` 类的属性，当然也是 `Human` 的实例的属性。那传递过去的参数 `cls` 是类还是实例呢？

    In [1]: class Human(object):
       ...:     weight = 12
       ...:     @classmethod
       ...:     def get_weight(cls):
       ...:         print cls 

    In [2]: Human.get_weight()
    <class '__main__.Human'>

    In [3]: Human().get_weight()
    <class '__main__.Human'>

我们看到传递过去的都是 `Human` 类,不是 `Human` 的实例，两种方式调用的结果没有任何区别。`cls` 只是一个普通的函数参数，调用时被隐含的传递过去。  
总结起来

1.  `classmethod` 是类与函数的结合。
3.  可以使用和类的实例调用，但是都是将类作为隐含参数传递过去。
2.  使用类来调用 `classmethod` 可以避免将类实例化的开销。

#### static method
