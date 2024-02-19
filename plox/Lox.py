import argparse
import sys
from Scanner import *
from Parser import *
from AstPrinter import *


class Lox:
    """
    Lox class
    """

    @classmethod
    def main(cls, args: argparse.Namespace) -> None:
        cls.had_error = False
        if args.name:
            print(f"run {args.name}")
            cls.__run_file(args.name)
        else:
            print("run prompt")
            cls.__run_prompt()

    @classmethod
    def __run_file(cls, name: str) -> None:
        source = str()
        with open(name, "r") as f:
            source = f.read()
        cls.__run(source)
        if cls.had_error:
            sys.exit(65)

    @classmethod
    def __run_prompt(cls) -> None:
        while True:
            line = input(">")
            if line == "exit()":
                break
            cls.__run(line)
            cls.had_error = False

    @classmethod
    def __run(cls, source: str) -> None:
        scanner = Scanner(source, cls.error)  # 순환 참조 방지
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token.to_string())
        parser = Parser(tokens, cls.error)  # 순환 참조 방지
        expression = parser.pasre()

        if cls.had_error:
            return

        print(AstPrinter().print(expression))

    @classmethod
    def __report(cls, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        cls.had_error = True

    @classmethod
    def error(cls, **kwargs):  # 메소드 오버로딩 대체
        message = kwargs["message"]
        if "line" in kwargs:
            line = kwargs["line"]
            cls.__report(line, "", message)
            pass
        elif "token" in kwargs:
            token = kwargs["token"]
            if token.token_type == TokenType.EOF:
                cls.__report(token.line, " at end", message)
            else:
                cls.__report(token.line, f" at '{token.lexeme}'", message)
        else:
            cls.__report(-1, "Unkonw", "Error")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="plox")
    parser.add_argument("name", help="The name of the file you want to run", nargs="?")
    Lox.main(parser.parse_args())
