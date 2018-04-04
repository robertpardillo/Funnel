from multiprocessing.managers import BaseManager, BaseProxy


class Manager(BaseManager):
    pass


def ClassFactory(_classType):
    class InteractiveObject(_classType):
        pass
    return InteractiveObject


class Proxy(BaseProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__')
    _executable_ = ('test2', 'x', 'y')

    def __getattr__(self, item):
        callMethod = object.__getattribute__(self, '_callmethod')
        return_object = callMethod('__getattribute__',(item,))
        #return_object = ClassFactory(type(return_object))
        return return_object

    def __setattr__(self, key, value):
        if key in self._executable_:
            callMethod = object.__getattribute__(self, '_callmethod')
            callMethod('__setattr__', (key, value))
        else:
            super(Proxy, self).__setattr__(key, value)
"""
    def set(self, string, value):
        spl = string.split('.')
        obj = self.__getattr__(spl[0])
        if len(spl)>1:
            executable_string = string[len(spl[0]):]
            exec('obj{}=value'.format(executable_string))
        else:
            obj = value
        self._set(spl[0], obj)

    def _set(self, key, value):
        callMethod = object.__getattribute__(self, '_callmethod')
        callMethod('__setattr__', (key, value))
"""


class SharedClass(object):
    def __init__(self, _class, manager=None):
        if not manager:
            self.manager = Manager()
        else:
            self.manager = manager

        self.manager.register(_class.__name__, _class,Proxy)
        self._class = _class
        self._start()

    def _start(self):
        self.manager.start()

    def __call__(self, *args, **kwargs):
        return self.manager.__getattribute__('{}'.format(self._class.__name__))(*args)
