import logging
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from uvicorn import run

from .config import SetupConfig, read_config_file
from .functions import FunctionStore
from .llm import LLM
from .run import InputMode, Run, RunStatus, save_run
from .runner import Runner
from .runs import RunInfo, RunStore
from .sandbox import get_sandbox_from_code_exec_mode
from .shape import Shape
from .store import ShapeInfo, ShapeStore

logger = logging.getLogger(__name__)


class Settigns(BaseSettings):
    partial_config_path: Path = Path.home() / ".config" / "partial"


settings = Settigns()


class State:
    run_store: RunStore
    shape_store: ShapeStore
    runner: Runner


state = State()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global state
    print("Starting up")
    shape_store_path = settings.partial_config_path / "shapes"
    function_store_path = settings.partial_config_path / "functions"
    run_store_path = settings.partial_config_path / "runs"

    state.run_store = RunStore(path=run_store_path)
    state.shape_store = ShapeStore(path=shape_store_path)

    setup_config = read_config_file(settings.partial_config_path / "setup.json")
    if setup_config is None:
        setup_config = SetupConfig()

    llm_instance = LLM(
        provider=setup_config.llm.value, config_path=settings.partial_config_path
    )
    sandbox = get_sandbox_from_code_exec_mode(
        setup_config.code_execution, settings.partial_config_path
    )
    function_store = FunctionStore(path=function_store_path)

    state.runner = Runner(
        llm=llm_instance,
        sandbox=sandbox,
        store=function_store,
        quiet=True,
        progress=False,
        output_file=None,
        input_schema=None,
        invalid_mode=None,
    )

    yield
    print("Shutting down")
    state.runner.terminate()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Partial API!", "settings": settings.model_dump()}


class SimpleShapeInfo(BaseModel):
    id: str
    name: str | None
    filename: str
    created_at: datetime
    updated_at: datetime


class ResponseShapes(BaseModel):
    shapes: list[SimpleShapeInfo]


@app.get("/shapes", description="List of shapes")
def read_shapes() -> ResponseShapes:
    global state

    shape_store = state.shape_store
    shape_infos = shape_store.list()
    simple_shape_infos = [
        SimpleShapeInfo(**shape.dict()) for shape in shape_infos if shape is not None
    ]
    return ResponseShapes(shapes=simple_shape_infos)


class ResponseShape(BaseModel):
    shape: ShapeInfo


@app.get("/shapes/{shape_id}")
def read_shape(shape_id: str):
    global state

    shape_store = state.shape_store
    shape_store.refresh()
    shape_info = shape_store.get_by_id(shape_id)
    if shape_info is None:
        raise HTTPException(status_code=404, detail="Shape not found")
    # TODO: Use ResponseShape, Problem with multiple version of pydantic
    return {"shape": shape_info}


class RequsetRun(BaseModel):
    data: list | dict


class ResponseRun(BaseModel):
    run_id: str
    run_status: RunStatus
    outputs: list | dict


class ResponseRunFailed(BaseModel):
    run_id: str
    run_status: Literal[RunStatus.FAILED]
    error: str
    outputs: list | dict | None


class RunFailedException(Exception):
    def __init__(self, body: ResponseRunFailed):
        self.body = body


@app.exception_handler(RunFailedException)
async def run_failed_exception_handler(request, exc):
    return JSONResponse(status_code=542, content=jsonable_encoder(exc.body))


@app.post(
    "/shapes/{shape_id}/run",
    responses={542: {"model": ResponseRunFailed, "description": "Run failed"}},
)
def shape_data(shape_id: str, body: RequsetRun) -> ResponseRun:
    global state

    shape_store = state.shape_store
    shape_store.refresh()
    shape_info = shape_store.get_by_id(shape_id)
    if shape_info is None:
        raise HTTPException(status_code=404, detail="Shape not found")

    shape = Shape().load(shape_info.content)
    runner = state.runner
    runner.store.refresh()

    run = Run(shape=shape, input_mode=InputMode.API)

    data = body.data
    if isinstance(data, dict):
        data = [data]

    run_res = runner.process(lines=data, run=run, return_outputs=True)

    save_run(run_res, state.run_store.path, quiet=True)

    if run_res.outputs is not None and len(run_res.outputs) == 1:
        outputs = run_res.outputs[0]
    else:
        outputs = run_res.outputs

    if run_res.status == RunStatus.FAILED:
        response = ResponseRunFailed(
            run_id=run_res.id,
            run_status=run_res.status,
            error="Run failed",
            outputs=outputs,
        )
        raise RunFailedException(body=response)

    return ResponseRun(run_id=run_res.id, run_status=run_res.status, outputs=outputs)


class ResponseRuns(BaseModel):
    runs: list[RunInfo]


@app.get("/shapes/{shape_id}/runs", description="List of runs for a shape")
def read_runs(shape_id: str) -> ResponseRuns:
    global state

    state.shape_store.refresh()
    shape_info = state.shape_store.get_by_id(shape_id)
    if shape_info is None:
        raise HTTPException(status_code=404, detail="Shape not found")

    runs = state.run_store.list()
    shape_runs = [run for run in runs if run.shape_id == shape_id]
    # sort by most recent created first
    shape_runs.sort(key=lambda x: x.created_at, reverse=True)
    return ResponseRuns(runs=shape_runs)


class API:
    host: str
    port: int

    def __init__(self, host: str = "127.0.0.1", port: int = 2121):
        self.host = host
        self.port = port

    def start(self):
        run(app, host=self.host, port=self.port)
