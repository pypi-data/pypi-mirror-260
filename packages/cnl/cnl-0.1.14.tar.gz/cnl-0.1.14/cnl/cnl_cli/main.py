import typer
from cnl.cnl_run import cnl_run
from typing_extensions import Optional

app = typer.Typer()


# @app.command("run")
def cnl_run_command(module_path: str, config_path: Optional[str] = None):
    cnl_run(module_path, config_path)


def main():
    typer.run(cnl_run_command)


if __name__ == "__main__":
    main()
    # typer.run(cnl_run_command)
