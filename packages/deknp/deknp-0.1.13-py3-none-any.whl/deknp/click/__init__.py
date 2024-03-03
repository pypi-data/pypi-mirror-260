import typer
from typing_extensions import Annotated
from ..core import execute_install, execute_package_sure, execute_server, run_plugin_yaml, clear_pkg_cache
from ..gen.tmpl import ShellGenerator

app = typer.Typer(add_completion=False)


@app.command()
def install():
    execute_install()


@app.command()
def sure(force: Annotated[bool, typer.Option("--force/--no-force")] = False):
    execute_package_sure(force)


@app.command()
def server():
    execute_server(False)


@app.command()
def serverfull():
    execute_server(True)


@app.command()
def clearcache():
    clear_pkg_cache()


@app.command()
def yaml():
    run_plugin_yaml()


@app.command()
def shell(path: Annotated[str, typer.Argument()] = "."):
    ShellGenerator(path, None).render()
