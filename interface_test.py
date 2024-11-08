from interface import implements, Interface


class IClass(Interface):
    def myFirstMethod(self, x):  raise NotImplementedError()
    def mySecondMethod(self, x): raise NotImplementedError()


class MyClass(implements(IClass)):
    def myFirstMethod(self, x):
        print(f"First method, {self}!")


c = MyClass()
c.myFirst_method()
c.mySecondMethod()
