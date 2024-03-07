import ast
import logging
import subprocess
import sys

import typer

logger = logging.getLogger(__name__)


def install(package):
    """Install a Python package using pip."""
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", package],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def is_package_installed(package):
    """Check if a Python package is installed."""
    try:
        results = subprocess.check_call(
            [sys.executable, "-m", "pip", "show", package], stdout=subprocess.DEVNULL
        )
        return results == 0
    except subprocess.CalledProcessError:
        return False


def is_library_importable(library_name):
    """Check if a library can be imported (i.e., is installed)."""
    importable = library_importable(library_name)
    if not importable:
        return is_package_installed(library_name)
    return True


def find_uninstalled_libraries(libraries) -> list[str]:
    """Return a list of libraries that are not installed or importable."""
    return [lib for lib in libraries if not is_library_importable(lib)]


def local_install_pip_packages(libs):
    """Prompt to install uninstalled libraries locally."""
    if not libs:
        logger.info("No packages specified for installation.")
        return

    uninstalled_libraries = find_uninstalled_libraries(libs)
    if not uninstalled_libraries:
        logger.info("All packages are already installed.")
        return

    if sys.stdin.isatty():
        # Interactive mode
        confirm_install = typer.confirm(
            f"Install packages locally: {' '.join(uninstalled_libraries)}?",
            default=True,
        )
        if not confirm_install:
            logger.info("Not installing packages.")
            raise typer.Abort()
    else:
        # Non-interactive mode
        typer.echo(
            f"You need to install packages locally first:\npip install {' '.join(uninstalled_libraries)}\n"
        )
        raise typer.Exit(1)

    for lib in uninstalled_libraries:
        install(lib)


def ast_check_if_importable(node):
    if isinstance(node, ast.ImportFrom):
        return library_importable(node.module)
    if isinstance(node, ast.Import):
        return library_importable(node.names[0].name.split(".")[0])
    return None


def ast_get_importable_libs(nodes):
    return [(ast_check_if_importable(node), node) for node in nodes]


def library_importable(library_name):
    """Check if a library is importable (i.e., installed)."""
    try:
        __import__(library_name)
        return True
    except ImportError:
        return False


def get_library_import_status(libraries) -> list[tuple[str, bool]]:
    """Return a list of tuples containing library names and their import status."""
    return [(lib, library_importable(lib)) for lib in libraries]
