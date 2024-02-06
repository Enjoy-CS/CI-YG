import argparse
from typing import List, TextIO

indent_size = "    "


class GenerateAst:
    """_summary_
    GenerateAst class
    """

    @classmethod
    def main(cls, args: argparse.Namespace) -> None:
        print(f"{args.output_dir=}")
        cls.__define_ast(
            args.output_dir,
            "Expr",
            [
                "Binary   / left : Expr, operator : Token, right : Expr",
                "Grouping / expression : Expr",
                "Literal  / value : object",
                "Unary    / operator : Token, right : Expr",
            ],
        )
        print("Generation complete!")

    @classmethod
    def __define_ast(cls, output_dir: str, base_name: str, types: List[str]) -> None:
        path = f"{output_dir}/{base_name}.py"
        with open(path, "w") as f:
            f.write("from Token import *\n")
            f.write("from typing import Any\n")
            f.write("\n")
            f.write(f"class {base_name}:\n")
            f.write(f'{indent_size}"""\n[abstract]\nExpr class\n"""\n')
            # f.write(f"{indent_size}def accept(self, visitor : Visitor) -> Any:\n")
            # type 선언 전에 hint를 주는 것이 불가능 함
            # 추후 개선
            f.write(f"{indent_size}def accept(self, visitor) -> Any:\n")
            f.write(f"{indent_size*2}pass\n")

            cls.__define_visitor(f, base_name, types)

            for type in types:
                ## 뭔가 좀 더 파이썬스러운 표현이 가능하지 않을까?
                class_name = type.split("/")[0].strip()
                fields = type.split("/")[1].strip()
                cls.__defin_type(f, base_name, class_name, fields)

    @classmethod
    def __defin_type(
        cls, f: TextIO, base_name: str, class_name: str, field_list: str
    ) -> None:
        f.write(f"class {class_name}({base_name}):\n")
        f.write(f"{indent_size}def __init__(self,{field_list}) -> None:\n")

        for field in field_list.split(", "):
            name = field.split(" : ")[0]
            f.write(f"{indent_size*2}self.{name}={name}\n")

        f.write(f"{indent_size}def accept(self, visitor : Visitor) -> Any:\n")
        f.write(f"{indent_size*2}return visitor.visit{class_name}{base_name}(self)\n")

    @classmethod
    def __define_visitor(cls, f: TextIO, base_name: str, types: List[str]) -> None:
        f.write("class Visitor:\n")
        f.write(f'{indent_size}"""\n[interface]\nVisitor class\n"""\n')

        for type in types:
            type_name = type.split("/")[0].strip()

            # f.write(
            #     f"{indent_size}def visit{type_name}{base_name}(self, {base_name.lower()} : {type_name}) -> Any:\n"
            # )
            # type 선언 전에 hint를 주는 것이 불가능 함
            # 추후 개선
            f.write(
                f"{indent_size}def visit{type_name}{base_name}(self, {base_name.lower()}) -> Any:\n"
            )
            f.write(f"{indent_size*2}pass\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gen ast tool")
    parser.add_argument("output_dir", help="The directory path to output the file")
    GenerateAst.main(parser.parse_args())
