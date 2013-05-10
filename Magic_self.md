Python的self参数使一些人特别恼怒。举例来说,你必须在每个类的方法里显示地定义它。它然后粗鲁地注入到了不想要他的地方。
    
    class Foo(object):
        x = 9
        def __init__(self,x):
            self.x = x
 
        def bar(self,y): 
            return self.x + y

如果你来自 C++, Java 或者其它相似的背景。self在`__init__`和`bar`
