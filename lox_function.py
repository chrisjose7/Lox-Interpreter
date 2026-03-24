from environment import Environment
from lox_callable import LoxCallable
from return_exception import ReturnException


class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)

        for i in range(len(self.declaration.params)):
            param_name = self.declaration.params[i].lexeme
            environment.define(param_name, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as ret:
            return ret.value

        return None

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"