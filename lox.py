import sys

from scanner import Scanner
from parser import Parser
from interpreter import Interpreter


had_error = False

interpreter = Interpreter()


def error(line, message):
    report(line, "", message)


def parser_error(line, where, message):
    report(line, where, message)


def report(line, where, message):
    global had_error
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
    had_error = True


def run(source):
    global had_error

    scanner = Scanner(source, error_reporter=error)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens, error_reporter=parser_error)
    statements = parser.parse()

    if had_error:
        return

    interpreter.interpret(statements)


def run_file(path):
    global had_error

    with open(path, "r", encoding="utf-8") as f:
        run(f.read())

    if had_error:
        sys.exit(65)


def run_prompt():
    global had_error

    while True:
        try:
            line = input("> ")
        except EOFError:
            break

        run(line)
        had_error = False


def main():
    if len(sys.argv) > 2:
        print("Usage: python3 lox.py [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()


if __name__ == "__main__":
    main()