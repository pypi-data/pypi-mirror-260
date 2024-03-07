from collections import defaultdict
from pathlib import Path

import typer
from langchain.pydantic_v1 import BaseModel
from tabulate import tabulate
from typing_extensions import Annotated

from ..store import ShapeInfo, ShapeStore

app = typer.Typer()


class ShapesOutput(BaseModel):
    """Represents the output structure for shapes."""

    location: Path
    shapes: list[ShapeInfo]


def display_shapes(
    shapes_output: ShapesOutput, all_: bool = True, full_path: bool = False
):
    """Displays the shape information in a formatted table.

    Args:
        shapes_output (ShapesOutput): The output object containing shape information.
        all_ (bool): If True, display all shapes. If False, display only the latest shape for each name.
    """
    if not shapes_output.shapes:
        print("Location:", shapes_output.location)
        print("No shapes to display.")
        return

    headers = ["SHAPE NAME", "ID", "FILENAME", "LAST UPDATED"]
    table = []

    # Group shapes by name
    shapes_by_name = defaultdict(list)
    for shape in shapes_output.shapes:
        shapes_by_name[shape.name].append(shape)

    for name, shapes in shapes_by_name.items():
        shapes = sorted(shapes, key=lambda x: x.updated_at, reverse=True)
        for i, shape in enumerate(shapes):
            if i == 0 or all_:
                updated_at_str = (
                    shape.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    if shape.updated_at
                    else "N/A"
                )
                filename = (
                    shape.filename
                    if not full_path
                    else shapes_output.location / shape.filename
                )
                row = [name if i == 0 else "", shape.id, filename, updated_at_str]
                table.append(row)

    print("Location:", shapes_output.location, "\n")
    print(tabulate(table, headers=headers, tablefmt="simple"))


def retrieve_shapes_data(config_path: Path) -> ShapesOutput:
    """Retrieves shape data from the given configuration path."""
    shapes_path = config_path / "shapes"
    store = ShapeStore(path=shapes_path)

    try:
        store.refresh()
    except Exception as e:
        print(f"Error refreshing the shape store: {e}")
        return ShapesOutput(location=shapes_path, shapes=[])

    return ShapesOutput(location=store.path, shapes=store.shape_infos)


@app.callback(invoke_without_command=True)
def list_shapes(
    ctx: typer.Context,
    json_output: Annotated[
        bool,
        typer.Option(
            "--json",
            "-j",
            help="Show the output in JSON format",
        ),
    ] = False,
    all_: Annotated[
        bool,
        typer.Option(
            "--all",
            "-a",
            help="Show all shapes, not just the latest shape for each name",
        ),
    ] = False,
    full_path: Annotated[
        bool,
        typer.Option("--full-path", "-f", help="Show the full path."),
    ] = False,
):
    """
    List all the available shapes.
    """
    config_path = Path(ctx.obj["config_path"])
    shapes_output = retrieve_shapes_data(config_path)

    if json_output:
        print(shapes_output.json(indent=4))
    else:
        display_shapes(shapes_output, all_, full_path)
