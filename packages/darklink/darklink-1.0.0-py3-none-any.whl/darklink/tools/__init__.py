import importlib
import pkgutil

import click


tools: dict[str, type] = {}


class Tool:
    """Base class for a Tool."""

    def __init_subclass__(cls, **kwargs):
        """Keep track of each subclass"""
        super().__init_subclass__(**kwargs)
        tools[cls.__name__.lower()] = cls

    def fetch(platform: str, arch: str) -> tuple[str, bytes]:
        pass


def load():
    """Dynamically import every module in the tools directory."""
    for _, name, _ in pkgutil.iter_modules(__path__, __name__ + "."):
        importlib.import_module(name)


def get_help_text():
    """Return the help documenting all the available tools."""
    return f"\b\nAvailable tools:\n  " + "\n  ".join([f"{x.__name__.ljust(15)} {x.__doc__}" for x in tools.values()])


def find(tool_name: str) -> Tool:
    """Find a tool by name."""

    try:
        tool = tools[tool_name.lower()]
    except KeyError:
        click.echo(f"Could not find: {tool_name}")
        print(get_help_text())
        exit(-1)

    return tool
