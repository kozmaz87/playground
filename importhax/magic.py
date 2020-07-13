
class ImportWrapper:

    __my_tf = None

    def __getattr__(self, item):
        if self.__my_tf is None:
            print('Importing tensorflow')
            import tensorflow
            self.__my_tf = tensorflow

        return getattr(self.__my_tf, item)


tf = ImportWrapper()
