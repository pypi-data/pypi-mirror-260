import typer
from typing import Optional, List
from typing_extensions import Annotated
from ..tmpl.render import render_dir

app = typer.Typer(add_completion=False)


@app.command()
def render(
        dest,
        src,
        file: Annotated[Optional[List[str]], typer.Option()] = None,
        _set: Annotated[Optional[List[str]], typer.Option('--set')] = None
):
    render_dir(dest, src, file, _set)
