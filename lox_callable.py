class LoxCallable:
    def arity(self):
        raise NotImplementedError

    def call(self, interpreter, arguments):
        raise NotImplementedError