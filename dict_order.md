先来看下这个程序

    #import time


    class A(object): pass
    class B(object): pass
    class C(object): pass
    class D(object): pass
    class E(object): pass
    class F(object): pass
    class G(object): pass
    class H(object): pass

    class Foo(object):
        d = {A: 1, B: 2, C: 3, D: 4,
             E: 5, F: 6, G: 7, H: 8}

        def bar(self):
            for key, value in self.d.iteritems():
                print key.__name__,

    f = Foo()
    f.bar()


在我的电脑上运行了很多次得到的结果都是 `B E F A G H D C`，但是当我取消掉第一行的注释,多次运行得到的结果都是`F G E H B A D C`。为什么仅仅加了一句无用的 `import time` 结果就发生变化了呢？

为了理解iteritems造成的不同顺序的原因，我们需要理解CPython中dict中的实现。

*   dict是以hash表为基础实现的
*   一个新的dict初始化为的时候有8个空间,数组只能存放8个对象（的指针），但是对于小的dict来说已经够用了。不够用时，才会自动调用malloc去申请内存空间。也就是说，对于很多条目较少的dict来说，创建它们减少了一次malloc的调用；而对于大dict来说，也不过就浪费了8个对象指针（约32字节）的空间而已。
*   当dict中加入新的条目的时候，
