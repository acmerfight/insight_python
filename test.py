def button(i, func):
    print "button ", i
    func()

for i in range(10):
    def callback():
        print "click", i
    button(i, callback)
