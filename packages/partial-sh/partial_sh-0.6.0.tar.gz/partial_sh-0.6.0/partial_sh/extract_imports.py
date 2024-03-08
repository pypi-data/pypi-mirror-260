import ast
import sys

from langchain.pydantic_v1 import BaseModel, Field


class LibrariesToInstall(BaseModel):
    libraries: list[str] = Field(description="The libraries to install")


class ImportExtractor(ast.NodeVisitor):
    def __init__(self, exclude_stdlib=False):
        self.imports_nodes = []
        if exclude_stdlib:
            self.stdlib_modules = (
                list(sys.stdlib_module_names)
                if hasattr(sys, "stdlib_module_names")
                else []
            )
        else:
            self.stdlib_modules = []

    def visit_Import(self, node):
        if self.stdlib_modules:
            for n in node.names:
                if n.name.split(".")[0] not in self.stdlib_modules:
                    self.imports_nodes.append(node)
        else:
            self.imports_nodes.append(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if self.stdlib_modules and node.module:
            if node.module.split(".")[0] not in self.stdlib_modules:
                self.imports_nodes.append(node)
        else:
            self.imports_nodes.append(node)
        self.generic_visit(node)


def extract_imports(code, exclude_stdlib=False):
    tree = ast.parse(code)
    visitor = ImportExtractor(exclude_stdlib=exclude_stdlib)
    visitor.visit(tree)
    if not visitor.imports_nodes:
        return None
    return visitor.imports_nodes


def convert_to_code(nodes):
    if not nodes:
        return None
    return ast.unparse(nodes)
