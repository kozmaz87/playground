
import importlib


class ImportWrapper:

    name = None
    __my_module = None

    def __init__(self, name):
        self.name = name

    def __getattr__(self, item):
        if self.__my_module is None:
            print('Importing {}'.format(self.name))
            self.__my_module = importlib.import_module(self.name)

        return getattr(self.__my_module, item)


tf = ImportWrapper('tensorflow')
