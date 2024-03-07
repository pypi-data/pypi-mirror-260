import logging
import os
from enum import Enum
from pathlib import Path

import typer
from e2b import CodeInterpreter

from .docker_sandbox import DockerSandbox, ErrorCodeExecution

logger = logging.getLogger(__name__)


class SandboxErrorCodeExecution(Exception):
    pass


def init_interpreter_e2b(config_path: Path):
    if "E2B_API_KEY" in os.environ:
        e2b_api_key = os.getenv("E2B_API_KEY")
    elif os.path.exists(config_path / "e2b_api_key"):
        with open(config_path / "e2b_api_key", "r") as f:
            e2b_api_key = f.read()
    else:
        print("E2B API key not found, please run:\npartial setup")
        raise typer.Exit(1)

    # Create interpreter instance
    interpreter = CodeInterpreter(api_key=e2b_api_key)
    return interpreter


class ProviderNotSupported(Exception):
    pass


class NotImplementedForProvider(Exception):
    pass


class SandboxMode(str, Enum):
    E2B = "e2b"
    DOCKER = "docker"
    NO = "no"  # Will be used for local execution


class Sandbox:
    """
    Sandbox to run code in a safe environment.

    Sandbox available:
    - e2b (Remote)
    - docker (Local)
    """

    provider = None
    interpreter: CodeInterpreter | DockerSandbox = None

    def __init__(
        self,
        provider=SandboxMode.E2B,
        config_path: Path = Path.home() / ".config" / "partial",
    ):
        self.provider = provider
        self.interpreter = self.connnect(config_path=config_path)

    def connnect(self, config_path: Path):
        if self.provider == SandboxMode.E2B:
            logger.info("Connecting to e2b")
            self.interpreter = init_interpreter_e2b(config_path)
            logger.info("Connected to e2b")
        elif self.provider == SandboxMode.DOCKER:
            logger.info("Connecting to docker")
            # TODO: Find a better way to get the path
            filepath = Path(os.path.join(os.path.dirname(__file__), "sandboxes"))
            self.interpreter = DockerSandbox(
                dockerfile=filepath / "Dockerfile.sandbox.python"
            )
            self.interpreter.start()
            logger.info("Connected to docker")
        else:
            raise ProviderNotSupported("Provider not supported")

        return self.interpreter

    def _run_e2b(self, code):
        logger.info("Running code in e2b remote")
        stdout, stderr, artifacts = self.interpreter.run_python(code)
        if stderr:
            logger.error(stderr)
            raise SandboxErrorCodeExecution(stderr)
        return stdout

    def _run_docker(self, code):
        logger.info("Running code in docker local container")
        try:
            return self.interpreter.run_code(code)
        except ErrorCodeExecution as e:
            raise SandboxErrorCodeExecution(e)

    def install_packages(self, packages):
        if self.provider == SandboxMode.DOCKER:
            self.interpreter.install_packages(packages)
        else:
            raise NotImplementedForProvider(
                f"Install packages not supported for this provider: {self.provider}"
            )

    def install_pip_packages(self, packages):
        if self.provider == SandboxMode.DOCKER:
            self.interpreter.install_pip_packages(packages)
        elif self.provider == SandboxMode.E2B:
            logger.info(f"Install pip packages not supported for e2b: {packages}")
            pass
        else:
            raise NotImplementedForProvider(
                f"Install pip packages not supported for this provider: {self.provider}"
            )

    def run(self, code):
        logger.info("Running code in sandbox")
        if self.provider == SandboxMode.E2B:
            return self._run_e2b(code)
        elif self.provider == "docker":
            return self._run_docker(code)
        else:
            raise ProviderNotSupported("Provider not supported")

    def close(self):
        logger.info("Closing sandbox")
        if self.provider == SandboxMode.E2B:
            self.interpreter.close()
        elif self.provider == "docker":
            self.interpreter.stop()
        logger.info("Sandbox closed")
