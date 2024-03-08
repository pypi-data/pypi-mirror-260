import json
from enum import Enum
from pathlib import Path
from typing import Optional

from langchain.pydantic_v1 import BaseModel


class LLMProvider(Enum):
    OPENAI = "openai"


class CodeExecutionProvider(Enum):
    LOCAL = "local"
    E2B = "e2b"
    DOCKER = "docker"


class SetupConfig(BaseModel):
    llm: LLMProvider = LLMProvider.OPENAI
    code_execution: CodeExecutionProvider = CodeExecutionProvider.LOCAL


def read_config_file(config_file: Path) -> Optional[SetupConfig]:
    setup_config = None

    # check if file exists
    if not config_file.exists() or not config_file.is_file():
        return None

    # check if end with .json
    if config_file.suffix != ".json":
        return None

    with (config_file).open("r") as f:
        setup_config = json.load(f)
        setup_config = SetupConfig(**setup_config)

    return setup_config
