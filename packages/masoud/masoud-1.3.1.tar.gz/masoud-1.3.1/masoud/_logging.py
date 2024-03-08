import sys

import click

RED = "\033[91m"
GREEN = "\033[92m"
GRAY = "\033[90m"
END = "\033[0m"


def ok(text: str) -> None:
    click.echo(f"{GRAY}(ok)   > {GREEN}{text}{END}", file=sys.stderr)


def debug(text: str) -> None:
    click.echo(f"{GRAY}(dbg)  > {text}{END}", file=sys.stderr)


def err(text: str, *context: str | bytes | Exception | None) -> None:
    click.echo(f"{GRAY}(err)  > {RED}{text}{END}", file=sys.stderr)
    for c in context:
        if c:
            click.echo(str(c).strip("\n"), file=sys.stderr)
