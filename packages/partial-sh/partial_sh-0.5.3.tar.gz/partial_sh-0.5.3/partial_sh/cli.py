import logging

from .commands.config import app as config_app
from .commands.functions import app as functions_app
from .commands.main import app as main_app
from .commands.runs import app as runs_app
from .commands.setup import app as setup_app
from .commands.shapes import app as shapes_app
from .commands.show import app as show_app

main_app.add_typer(setup_app, name="setup", no_args_is_help=False, help="Setup partial")
main_app.add_typer(config_app, name="config", no_args_is_help=False, help="Config")
main_app.add_typer(
    functions_app, name="functions", no_args_is_help=False, help="Functions"
)
main_app.add_typer(shapes_app, name="shapes", no_args_is_help=False, help="Shapes")
main_app.add_typer(
    show_app, name="show", no_args_is_help=True, help="Show the content of a shape"
)
main_app.add_typer(runs_app, name="runs", no_args_is_help=False, help="Runs")


def main():
    main_app()


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    main()
