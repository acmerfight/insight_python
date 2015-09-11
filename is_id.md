### (ob1 is ob2) 等价于 (id(ob1) == id(ob2))
首先 id 函数可以获得对象的内存地址，如果两个对象的内存地址是一样的，那么这两个对象肯定是一个对象。和 is 是等价的。Python 源代码为证。

    4451 static PyObject *
    4452 cmp_outcome(int op, register PyObject *v, register PyObject *w)
    4453 {
    4454     int res = 0;
    4455     switch (op) {
    4456     case PyCmp_IS:
    4457         res = (v == w);
    4458         break;
    4459     case PyCmp_IS_NOT:
    4460         res = (v != w);
    4461         break;

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

两个对象用`is`判断是`False`，用`id`判断却是`True`，这与我们已知的事实不符啊，这种现象该如何解释呢？遇到这种情况最好的解决方法就是调用 dis 模块去看下两个比较语句到底做了什么。

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

真实情况是当执行`.`操作符的时候，实际是生成了一个 proxy 对象，`foo.bar is Foo.bar`的时候，两个对象顺序生成，放在栈里相比较，由于地址不同肯定是`False`，但是`id(foo.bar) == id(Foo.bar)`的时候就不同了，首先生成`foo.bar`,然后计算`foo.bar`的地址，计算完之后`foo.bar`的地址之后，就没有任何对象指向`foo.bar`了，所以`foo.bar`对象就会被释放。然后生成`Foo.bar`对象，由于`foo.bar`和`Foo.bar`所占用的内存大小是一样的，所以又恰好重用了原先`foo.bar`的内存地址，所以`id(foo.bar) == id(Foo.bar)`的结果是`True`。

下面内容由邮件`Leo Jay`大牛提供，他解释的更加通透。

用`id(expression a) == id(expression b)`来判断两个表达式的结果是不是同一个对象的想法是有问题的。 

`foo.bar` 这种形式叫 attribute reference [1]，它是表达式的一种。`foo`是一个instance object,`bar`是一个方法，这个时候表达式`foo.bar`返回的结果叫method object [2]。根据文档： 

    When an instance attribute is referenced that isn’t a data attribute, 
    its class is searched. If the name denotes a valid class attribute 
    that is a function object, a method object is created by packing 
    (pointers to) the instance object and the function object just found 
    together in an abstract object: this is the method object. 

`foo.bar`本身并不是简单的名字，而是表达式的计算结果，是一个 method object，在`id(foo.bar)`这样的表达式里，method object只是一个临时的中间变量而已，对临时的中间变量做`id`是没有意义的。  
一个更明显的例子是，

    print id(foo.bar) == id(foo.__init__)

输出的结果也是`True` 

看 id 的文档[3]： 

    Return the “identity” of an object. This is an integer (or long 
    integer) which is guaranteed to be unique and constant for this object 
    during its lifetime. Two objects with non-overlapping lifetimes may 
    have the same id() value. 
    CPython implementation detail: This is the address of the object in memory.

只有你能保证对象不会被销毁的前提下，你才能用 id 来比较两个对象。所以，如果你非要比的话，得这样写：  

    fb = foo.bar 
    Fb = Foo.bar 
    print id(fb) == id(Fb) 

即把两个表达式的结果绑定到名字上，再来比是不是同一个对象，你才能得到正确的结果。 

`is`表达式 [4] 也是一样的，你现在得到了正确的结果，完全是因为 CPython 现在的实现细节决定的。现在的`is`的实现，是左右两边的对象都计算出来，然后再比较这两个对象的地址是否一样。万一哪天改成了，先算左边，保存地址，把左边释放掉，再算右边，再比较的话，你的`is`的结果可能就错了。官方文档里也提到了这个问题 [5]。我认为正确的方法也是像`id`那样，先把左右两边都计算下来，并显式绑定到各自的名字上，然后再用`is`判断。 

[1] http://docs.python.org/2/reference/expressions.html#attribute-references   
[2] http://docs.python.org/2/tutorial/classes.html#method-objects  
[3] http://docs.python.org/2/library/functions.html#id  
[4] http://docs.python.org/2/reference/expressions.html#index-68  
[5] http://docs.python.org/2/reference/expressions.html#id26   
