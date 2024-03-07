#!/usr/bin/env python3
"""Generates the README.md file at the root of this repository"""

import inspect
import os
from string import Template

import click

import masoud

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
README_TARGET_FILE = os.path.join(PROJECT_ROOT, "README.md")
README_TEMPLATE_FILE = os.path.join(PROJECT_ROOT, "tools/README.template.md")

with open(README_TEMPLATE_FILE, "r") as f:
    README_TEMPLATE = Template(f.read())


if __name__ == "__main__":
    methods = [
        property
        for name, property in inspect.getmembers(masoud.Service)
        if inspect.isfunction(property) and not name.startswith("_")
    ]

    api = "```python"
    for method in methods:
        api += f"\ndef {method.__name__}{inspect.signature(method)}:\n"
        api += f'    """{method.__doc__}"""\n'
    api += "```\n"

    help = masoud.cli.get_help(click.Context(masoud.cli))

    readme = README_TEMPLATE.safe_substitute(api=api, help=help)
    with open(README_TARGET_FILE, "w") as f:
        f.write(readme)
