import subprocess

import typer


class DemoCase:
    title: str
    commands: list[str]

    def __init__(self, title: str, commands: list[str]):
        self.title = title
        self.commands = commands


def execute_demo(demo: DemoCase):
    prep_comamnds = "\n".join(["$ " + cmd for cmd in demo.commands])
    msg = f"[DEMO: {demo.title}]\n\n{prep_comamnds}\n\nDo you want to run the command"
    should_run = typer.confirm(msg, abort=True, default=True)
    if not should_run:
        raise typer.Exit(1)
    print("Running the command...\n---")
    for command in demo.commands:
        subprocess.run(command, shell=True)
    print("\n")


def execute_demos(demos: list[DemoCase]):
    for idx, demo in enumerate(demos):
        execute_demo(demo)
        if idx < len(demos) - 1:
            next_demo = typer.confirm("Next demo", abort=True, default=True)
            if not next_demo:
                raise typer.Exit(1)


def run_demos():
    """
    Run the demos
    """
    demo1 = DemoCase(
        title="Pipe as input",
        commands=[
            """echo '{"name":"Jay Neal", "address": "42 Main St 94111"}' | pt -i 'Split firstname and lastname' -i 'remove the address'"""
        ],
    )
    demo2 = DemoCase(
        title="Multi lines with JSON Lines",
        commands=[
            """cat << EOF > data.jsonl
{"name":"John Doe","date_of_birth":"1980-01-01", "address": "123 Main St"}
{"name":"Jane Smith","date_of_birth":"1990-02-15", "address": "456 Main St"}
{"name":"Jay Neal","date_of_birth":"1993-07-27", "address": "42 Main St 94111"}
{"name":"Lisa Ray","date_of_birth":"1985-03-03", "address": "789 Elm St"}
EOF""",
            """pt --file data.jsonl -i 'Split firstname and lastname' -i 'remove the address'""",
        ],
    )
    execute_demos([demo1, demo2])
