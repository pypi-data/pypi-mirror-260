# Docker sandbox
# - Build image
# - Start container
# - Upload code
# - Execute code
# - Stop container

import io
import logging
import os
import tarfile
from pathlib import Path

import docker
import typer
from docker import DockerClient
from docker.errors import APIError, BuildError, DockerException
from docker.models.containers import Container

logger = logging.getLogger(__name__)


class ErrorCodeExecution(Exception):
    pass


class DockerSandbox:
    client: DockerClient
    dockerfile: Path
    image_name: str
    container_name: str
    ctr: Container = None

    def __init__(
        self,
        dockerfile: str,
        image_name: str = "partial-code:latest",
        container_name: str = "partial-code",
    ):
        self.dockerfile = dockerfile
        self.image_name = (
            image_name if image_name.endswith(":latest") else f"{image_name}:latest"
        )
        self.container_name = container_name
        try:
            self.client = docker.from_env()
        except DockerException:
            logger.error(
                "Error connecting to Docker. Check if Docker is installed and running."
            )
            raise typer.Exit(1)

    def start(self):
        self.init_cleanup()
        self.build_image()
        self.ctr = self.run_container()

    def stop(self):
        self.ctr.stop()

    def init_cleanup(self):
        try:
            container = self.client.containers.get(self.container_name)
        except docker.errors.NotFound:
            logging.debug(f"Container {self.container_name} not found")
            return
        container.stop()

    def build_image(self):
        try:
            img, _ = self.client.images.build(
                path=".", dockerfile=self.dockerfile, tag=self.image_name
            )
        except BuildError as e:
            logger.error(f"Error building image: {e}")
            raise e
        except APIError as e:
            logger.error(f"Error building image: {e}")
            raise e
        return img.id

    def run_container(self):
        container = self.client.containers.run(
            image=self.image_name,
            command=["/bin/bash"],
            stderr=True,
            name=self.container_name,
            remove=True,
            tty=False,
            stdin_open=True,
            detach=True,
        )
        return container

    def install_packages(self, packages: list):
        self.ctr.exec_run(cmd=["apt-get", "update"])
        self.ctr.exec_run(cmd=["apt-get", "install", "-y", *packages])

    def install_pip_packages(self, packages: list):
        self.ctr.exec_run(cmd=["pip", "install", *packages])

    def create_tarfile(self, filename: str, content: str):
        content_utf8 = content.encode("utf-8")
        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
            tarinfo = tarfile.TarInfo(filename)
            tarinfo.size = len(content_utf8)
            tar.addfile(tarinfo, io.BytesIO(content_utf8))
        return tar_buffer

    def upload_content(self, content: str, filepath: str):
        dstname = os.path.basename(filepath)
        dstdir = os.path.dirname(filepath)
        code_tar = self.create_tarfile(dstname, content)
        self.ctr.put_archive(dstdir, code_tar.getvalue())
        code_tar.close()

    def run_code(self, code: str):
        user = "partial"
        workdir = f"/home/{user}"
        filename = "program.py"
        filepath = f"{workdir}/{filename}"
        self.upload_content(code, filepath)
        exit_code, output = self.ctr.exec_run(
            cmd=["python3", filename], workdir=workdir
        )
        output = output.decode("utf-8")
        if exit_code != 0:
            raise ErrorCodeExecution(
                f"Error executing code: {exit_code} Message: {output}"
            )
        return output
