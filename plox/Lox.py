import argparse
import sys
from Scanner import *


class Lox:
    """_summary_
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
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token.to_string())
        print()

    @classmethod
    def error(cls, line: int, message: str):
        cls.__report(line, "", message)

    @classmethod
    def __report(cls, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="plox")
    parser.add_argument("name", help="The name of the file you want to run", nargs="?")
    a = parser.parse_args()
    Lox.main(parser.parse_args())
