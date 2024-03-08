import typer

from ..api import API

app = typer.Typer()


@app.callback(invoke_without_command=True)
def serve(
    ctx: typer.Context,
    host: str = typer.Option("127.0.0.1", help="Host to serve on"),
    port: int = typer.Option(2121, help="Port to serve on"),
):
    print("Starting the API server...")

    # TODO: Get the config path from the context, pass it to the API
    # config_path = Path(ctx.obj["config_path"])

    api = API(host=host, port=port)

    api.start()
