import json
from pathlib import Path

from pydantic import BaseModel


class RunInfo(BaseModel):
    id: str
    shape_id: str
    start_time: str | None = None
    end_time: str | None = None
    duration_sec: float | None = None
    status: str
    input_mode: str
    created_at: str
    updated_at: str


class RunsOutput(BaseModel):
    location: Path
    runs: dict[str, RunInfo] = {}


class RunStore:
    path: Path
    run_infos: list[RunInfo] = []

    def __init__(self, path: Path):
        self.path = path

    def refresh(self):
        self.run_infos = []
        self.list()

    def list(self) -> list[RunInfo]:
        for filename in self.path.iterdir():
            if filename.suffix == ".json":
                with open(self.path / filename, "r") as f:
                    run_info = json.load(f)
                    run_info = RunInfo.model_validate(run_info)
                    self.run_infos.append(run_info)
        return self.run_infos
