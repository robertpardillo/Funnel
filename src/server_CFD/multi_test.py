
import multiprocessing
from multiprocessing.managers import BaseManager, BaseProxy, NamespaceProxy
from sharedClass import SharedClass


class Test2(object):
    def __init__(self, x, y, z):
        self.__setattr__('x', x+10)
        self.__setattr__('y', y+10)
        self.__setattr__('z', z+10)

    def __setattr__(self, key, value):
        #print(key, 'Set test2')
        super(Test2, self).__setattr__(key, value)


class Test(object):
    def __init__(self,x,y,z):
        self.__setattr__('x', int(x))
        self.__setattr__('y', y)
        self.__setattr__('z', z)
        self.__setattr__('test2', Test2(x,y,z))

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        #print(key, 'Set test')
        super(Test, self).__setattr__(key, value)


def change1(obj,obj2):
    #obj.x = 50
    obj.set('x', 50)
    #obj.test2.x = 60
    #obj.y = 100
    obj.set('test2.x', 60)
    obj2.set('test2.y', 120)


def change2(obj, obj2):

    #obj.set('x', 80)
    pass


if __name__ == '__main__':

    # creating a list in server process memory
    """
    sessionManager.register('Test',Test, Test_Proxy)
    manager = sessionManager()
    manager.start()
    """
    shar = SharedClass(Test)
    obj = shar(10,20,30)
    obj2 = shar(50,60,80)
    # new record to be inserted in records

    # creating new processes
    p1 = multiprocessing.Process(target=change1, args=(obj,obj2))
    p2 = multiprocessing.Process(target=change2, args=(obj,obj2))

    # running process p1 to insert new record
    p1.start()
    p1.join()

    # running process p2 to print records
    p2.start()
    p2.join()

    print(obj.test2.x, obj.x, obj2.test2.y)