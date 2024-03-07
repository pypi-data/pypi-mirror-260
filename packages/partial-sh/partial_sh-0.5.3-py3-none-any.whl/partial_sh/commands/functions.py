from pathlib import Path

import typer
from langchain.pydantic_v1 import BaseModel
from typing_extensions import Annotated

from ..functions import FunctionItem, FunctionStore

app = typer.Typer()

# Constants
ID_WIDTH = 13
NAME_WIDTH = 500
NAME_LIMIT = 27
ELLIPSIS = "..."


class FunctionsOutput(BaseModel):
    location: Path
    functions: dict[str, FunctionItem] = {}


def retrieve_function_store_data(functions_path: Path) -> FunctionsOutput:
    store = FunctionStore(path=functions_path)

    try:
        store.refresh()
    except Exception as e:
        print(f"Error refreshing the function store: {e}")
        return FunctionsOutput(location=functions_path)

    return FunctionsOutput(location=functions_path, functions=store.functions)


def display_functions(functions_output: FunctionsOutput, full_path: bool = False):
    functions_path = functions_output.location
    function_infos = functions_output.functions

    if not function_infos:
        print("No functions found.")
        return

    print(f"Location: {functions_path}\n")
    print("FUNCTION NAME")

    infos = sorted(function_infos.values(), key=lambda x: x.name)
    for info in infos:
        name = info.name
        name_formatted = (
            (name[:NAME_LIMIT] + ELLIPSIS) if len(name) > NAME_WIDTH else name
        )
        if full_path:
            print(f"- {functions_path / info.filename}")
        else:
            print(f"- {name_formatted}")


@app.callback(invoke_without_command=True)
def list(
    ctx: typer.Context,
    json_output: Annotated[
        bool,
        typer.Option(
            "--json",
            "-j",
            help="Show the output in JSON format",
        ),
    ] = False,
    full_path: Annotated[
        bool,
        typer.Option("--full-path", "-f", help="Show the full path."),
    ] = False,
):
    """
    List the functions in the store.
    """
    config_path = Path(ctx.obj["config_path"])
    functions_path = config_path / "functions"

    functions_output = retrieve_function_store_data(functions_path)

    if json_output:
        print(functions_output.json(indent=4))
    else:
        display_functions(functions_output, full_path=full_path)
