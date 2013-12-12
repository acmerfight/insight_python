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
    In [7]: Human.get_weight()
    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)
    /home/yao/learn/insight_python/<ipython-input-7-a2b2c5cd2f8d> in <module>()
    ----> 1 Human.get_weight()

    TypeError: unbound method get_weight() must be called with Human instance as first argument (got nothing instead)


#### class method

#### static method
