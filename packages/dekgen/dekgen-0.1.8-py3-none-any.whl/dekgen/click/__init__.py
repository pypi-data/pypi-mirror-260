import typer
from typing import Optional, List
from typing_extensions import Annotated
from dektools.typer import multi_options_to_dict
from ..tmpl.render import render_dir

app = typer.Typer(add_completion=False)


@app.command()
def render(
        dest,
        src,
        file: Annotated[Optional[List[str]], typer.Option()] = None,
        _set: Annotated[Optional[List[str]], typer.Option('--set')] = None
):
    render_dir(dest, src, file, multi_options_to_dict(_set))


@app.callback()
def callback():
    pass
