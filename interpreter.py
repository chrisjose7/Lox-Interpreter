# Interpreter based on the tree-walk interpreter design from Crafting Interpreters
# I used ChatGPT to help translate and clarify parts of the logic.

from tokens import TokenType
from environment import Environment
from runtime_error import RuntimeError
from return_exception import ReturnException
from lox_function import LoxFunction

from expr import (
    Binary,
    Grouping,
    Literal,
    Unary,
    Variable,
    Assign,
    Logical,
    Call,
)

from stmt import (
    ExpressionStmt,
    PrintStmt,
    VarStmt,
    BlockStmt,
    IfStmt,
    WhileStmt,
    FunctionStmt,
    ReturnStmt,
)


class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            print(f"{error.message}\n[line {error.token.line}]")

    def execute(self, stmt):
        if isinstance(stmt, ExpressionStmt):
            self.evaluate(stmt.expression)

        elif isinstance(stmt, PrintStmt):
            value = self.evaluate(stmt.expression)
            print(self.stringify(value))

        elif isinstance(stmt, VarStmt):
            value = None
            if stmt.initializer is not None:
                value = self.evaluate(stmt.initializer)
            self.environment.define(stmt.name.lexeme, value)

        elif isinstance(stmt, BlockStmt):
            self.execute_block(stmt.statements, Environment(self.environment))

        elif isinstance(stmt, IfStmt):
            if self.is_truthy(self.evaluate(stmt.condition)):
                self.execute(stmt.then_branch)
            elif stmt.else_branch is not None:
                self.execute(stmt.else_branch)

        elif isinstance(stmt, WhileStmt):
            while self.is_truthy(self.evaluate(stmt.condition)):
                self.execute(stmt.body)

        elif isinstance(stmt, FunctionStmt):
            function = LoxFunction(stmt, self.environment)
            self.environment.define(stmt.name.lexeme, function)

        elif isinstance(stmt, ReturnStmt):
            value = None
            if stmt.value is not None:
                value = self.evaluate(stmt.value)
            raise ReturnException(value)

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def evaluate(self, expr):
        if isinstance(expr, Literal):
            return expr.value

        if isinstance(expr, Grouping):
            return self.evaluate(expr.expression)

        if isinstance(expr, Unary):
            right = self.evaluate(expr.right)

            if expr.operator.type == TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)

            if expr.operator.type == TokenType.BANG:
                return not self.is_truthy(right)

        if isinstance(expr, Binary):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)

            t = expr.operator.type

            if t == TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) - float(right)

            if t == TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return float(left) / float(right)

            if t == TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)

            if t == TokenType.PLUS:
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                raise RuntimeError(expr.operator, "Operands must be two numbers or two strings.")

            if t == TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right)

            if t == TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)

            if t == TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)

            if t == TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)

            if t == TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)

            if t == TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)

        if isinstance(expr, Variable):
            return self.environment.get(expr.name)

        if isinstance(expr, Assign):
            value = self.evaluate(expr.value)
            self.environment.assign(expr.name, value)
            return value

        if isinstance(expr, Logical):
            left = self.evaluate(expr.left)

            if expr.operator.type == TokenType.OR:
                if self.is_truthy(left):
                    return left
            else:
                if not self.is_truthy(left):
                    return left

            return self.evaluate(expr.right)

        if isinstance(expr, Call):
            callee = self.evaluate(expr.callee)
            arguments = [self.evaluate(arg) for arg in expr.arguments]

            if not hasattr(callee, "call") or not hasattr(callee, "arity"):
                raise RuntimeError(expr.paren, "Can only call functions.")

            if len(arguments) != callee.arity():
                raise RuntimeError(
                    expr.paren,
                    f"Expected {callee.arity()} arguments but got {len(arguments)}."
                )

            return callee.call(self, arguments)

        return None

    def is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def is_equal(self, a, b):
        return a == b

    def check_number_operand(self, operator, operand):
        if isinstance(operand, (int, float)):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise RuntimeError(operator, "Operands must be numbers.")

    def stringify(self, value):
        if value is None:
            return "nil"

        if isinstance(value, bool):
            return "true" if value else "false"

        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text

        return str(value)