"""Build function."""
import subprocess
import typer

from typing import Annotated, Optional


from ou_container_builder.cli.base import app
from ou_container_builder.cli.generate import generate
from ou_container_builder.cli.clean import clean


@app.command()
def build(
    tag: Annotated[Optional[list[str]], typer.Option(help="Docker tags to use")] = None,
    cache: Annotated[Optional[bool], typer.Option(help="Cache intermediate layers (true)")] = True,
) -> None:
    """Build the container image."""
    generate()
    cmd = ["buildah", "build", "--jobs", "2"]
    if tag is not None:
        for t in tag:
            cmd.extend(["--tag", t])
    if cache:
        cmd.extend(["--layers"])
    cmd.append(".")
    process = subprocess.run(cmd)
    if process.returncode == 0:
        clean()
