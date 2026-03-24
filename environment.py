from runtime_error import RuntimeError


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def get(self, name_token):
        if name_token.lexeme in self.values:
            return self.values[name_token.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(name_token)

        raise RuntimeError(name_token, f"Undefined variable '{name_token.lexeme}'.")

    def assign(self, name_token, value):
        if name_token.lexeme in self.values:
            self.values[name_token.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name_token, value)
            return

        raise RuntimeError(name_token, f"Undefined variable '{name_token.lexeme}'.")