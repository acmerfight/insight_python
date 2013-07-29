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
