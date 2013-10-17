### (ob1 is ob2) 等价于 (id(ob1) == id(ob2))
首先id函数可以获得对象的内存地址，如果两个对象的内存地址是一样的，那么这两个对象肯定是一个对象。和is是等价的。Python源代码为证。


但是请看下边代码的这种情况怎么会出现呢？
    
    In [1]: def bar(self, x):
    ...:     return self.x + y
    ...: 
 
    In [2]: class Foo(object):
    ...:     x = 9
    ...:     def __init__(self ,x):
    ...:         self.x = x
    ...:     bar = bar
    ...:     
 
    In [3]: foo = Foo(5)
 
    In [4]: foo.bar is Foo.bar
    Out[4]: False
 
    In [5]: id(foo.bar) == id(Foo.bar)
    Out[5]: True

两个对象用`is`判断是`False`，用`id`判断却是`True`，这与我们已知的事实不符啊，这种现象该如何解释呢？遇到这种情况最好的解决方法就是调用dis模块去看下两个比较语句到底做了什么。

    In [7]: dis.dis("id(foo.bar) == id(Foo.bar)")
              0 BUILD_MAP       10340
              3 BUILD_TUPLE     28527
              6 <46>           
              7 DELETE_GLOBAL   29281 (29281)
             10 STORE_SLICE+1  
             11 SLICE+2        
             12 DELETE_SUBSCR  
             13 DELETE_SUBSCR  
             14 SLICE+2        
             15 BUILD_MAP       10340
             18 PRINT_EXPR     
             19 JUMP_IF_FALSE_OR_POP 11887
             22 DELETE_GLOBAL   29281 (29281)
             25 STORE_SLICE+1  

    In [8]: dis.dis("foo.bar is Foo.bar")
              0 BUILD_TUPLE     28527
              3 <46>           
              4 DELETE_GLOBAL   29281 (29281)
              7 SLICE+2        
              8 BUILD_MAP        8307
             11 PRINT_EXPR     
             12 JUMP_IF_FALSE_OR_POP 11887
             15 DELETE_GLOBAL   29281 (29281)
用`id`
