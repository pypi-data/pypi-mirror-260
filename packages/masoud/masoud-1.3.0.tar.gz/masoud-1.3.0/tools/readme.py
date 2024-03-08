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
    methods = []
    for name, member in inspect.getmembers(masoud.Service):
        if inspect.isfunction(member) and not name.startswith("_"):
            methods.append(member)

    api = ""
    for method in methods:
        api += "```python\n"
        api += f"def {method.__name__}{inspect.signature(method)}:\n"
        api += "```\n\n"
        api += f"{inspect.getdoc(method)}\n\n"

    help = masoud.cli.get_help(click.Context(masoud.cli))

    readme = README_TEMPLATE.safe_substitute(api=api, help=help)
    with open(README_TARGET_FILE, "w") as f:
        f.write(readme)
