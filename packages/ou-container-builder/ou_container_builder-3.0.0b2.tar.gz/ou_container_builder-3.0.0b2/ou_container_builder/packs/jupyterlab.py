"""Functionality to install JupyterLab."""
from pydantic import BaseModel
from typing import Literal

from rich.progress import Progress

from ou_container_builder.state import State

name = "jupyterlab"


class Options(BaseModel):
    """Options for the JupyterLab pack."""

    version: Literal[3] | Literal[4] = 4


def init(state: State) -> None:
    """Initialise packs.jupyterlab."""
    if state["packs"]["jupyterlab"]["version"] == 3:
        state.update({"packages": {"pip": {"system": ["jupyterlab>=3.4.3,<4"]}}})
    elif state["packs"]["jupyterlab"]["version"] == 4:
        state.update({"packages": {"pip": {"system": ["jupyterlab>=4.0.2,<5"]}}})


def generate(state: State, progress: Progress) -> None:
    """Unused."""
    pass
