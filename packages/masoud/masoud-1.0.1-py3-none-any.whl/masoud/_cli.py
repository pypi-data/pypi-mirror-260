import json
import subprocess
import sys
from collections.abc import Callable
from functools import update_wrapper

import click

from ._inventory import Inventory, Group, Host
from ._service import Service


def green(text: str) -> str:
    return f"masoud > \033[92;1m{text}\033[0m"


def red(text: str) -> str:
    return f"masoud > \033[91;1m{text}\033[0m"


class CliWrapper(click.Group):
    def __init__(self, cli: click.Group) -> None:
        super().__init__(None, cli.commands)
        self.params = cli.params
        self.callback = cli.callback

    def __call__(self, services: list[Service], *args, **kwargs):
        return super().__call__(*args, **kwargs, obj={"services": services})


@click.group
@click.option(
    "--inventory",
    "-i",
    type=str,
    default="inventory.toml",
    help="Path to the inventory TOML file (default: inventory.toml)",
)
@click.option(
    "--group",
    "-g",
    type=str,
    default=None,
    help="Inventory group to operate on, default is set through `default_group` key",
)
@click.pass_context
def cli(ctx: click.Context, inventory: str, group: str | None) -> None:
    try:
        inv = Inventory(inventory)
    except Exception as e:
        click.echo(red("Could not read inventory!"))
        click.echo(e)
        sys.exit(1)

    group = group or inv.get_var("default_group", str)
    if group is None:
        click.echo(
            red(
                "No group (--group) given and no `default_group` inventory-level property set!"
            )
        )
        sys.exit(1)

    grp = inv.get_group(group)
    if grp is None:
        click.echo(red(f"Could not find group {group} in inventory"))
        sys.exit(1)

    ctx = click.get_current_context()
    ctx.obj["inventory"] = inv
    ctx.obj["group"] = grp


def pass_group(f: Callable) -> Callable:
    @click.pass_context
    def inner(ctx: click.Context, *args, **kwargs):
        group: Group = ctx.obj["group"]
        return ctx.invoke(f, *args, **kwargs, group=group)

    return update_wrapper(inner, f)


def resolve_host(ctx: click.Context, _param: str, value: str) -> Host:
    group: Group = ctx.obj["group"]
    host = group.get_host(value)
    if host is None:
        click.echo(red(f"Host {value} does not exist in group {group.name}."))
        sys.exit(1)
    return host


def resolve_hosts(ctx: click.Context, _param: str, value: list[str]) -> list[Host]:
    group: Group = ctx.obj["group"]
    if not value:
        return group.get_hosts()
    hosts = []
    for name in value:
        host = group.get_host(name)
        if host is None:
            click.echo(red(f"Host {value} does not exist in group {group.name}."))
            sys.exit(1)
        hosts.append(host)
    return hosts


def resolve_service(ctx: click.Context, _param: str, value: str) -> Service:
    services: list[Service] = ctx.obj["services"]
    for service in services:
        if service.name() == value:
            return service
    click.echo(red(f"Service {value} does not exist."))
    sys.exit(1)


@cli.command(name="ssh")
@click.argument("host", type=str, required=True, callback=resolve_host)
@click.argument("args", type=str, nargs=-1)
def ssh_cmd(host: Host, args: list[str]) -> None:
    """Connect to HOST via SSH."""
    result = subprocess.run(
        host._command_prefix + ["-t"] if len(args) < 1 else list(args)
    )
    if result.returncode != 0:
        sys.exit(result.returncode)


@cli.command(name="build")
@click.argument("service", type=str, required=True, callback=resolve_service)
@pass_group
def build_cmd(service: Service, group: Group) -> None:
    """Build the docker image for SERVICE, if needed."""
    with service._with_group(group):
        if service.dockerfile() is None:
            click.echo(
                f"Service {service.name()} has no Dockerfile and will not be built."
            )
            return
        result = subprocess.run(service._build_command)
    if result.returncode != 0:
        sys.exit(result.returncode)


@cli.command(name="deploy")
@click.argument("service", type=str, required=True, callback=resolve_service)
@click.argument("hosts", type=str, nargs=-1, callback=resolve_hosts)
@click.option(
    "--no-build",
    is_flag=True,
    type=bool,
    default=False,
    help="Don't build the image before deploying",
)
@click.pass_context
def deploy_cmd(
    ctx: click.Context, service: Service, hosts: list[Host], no_build: bool
) -> None:
    """Deploy SERVICE on HOSTS.
    This involves either building using the service's Dockerfile and copying it to the hosts
    or pulling the pre-built image on the hosts directly."""
    if not no_build:
        ctx.invoke(build_cmd, service=service)
    for host in hosts:
        with service._with_host(host):
            image = service.image()
            if service.dockerfile() is None:
                result = subprocess.run(host._command_prefix + service._pull_command)
                if result.returncode != 0:
                    click.echo(red(f"Failed to pull image {image} on {host.name}!"))
                    sys.exit(result.returncode)
                click.echo(green(f"Pulled image {image} on {host.name}"))
            elif host.ssh is not None:
                result = subprocess.run(
                    [
                        "bash",
                        "-c",
                        f"docker save {image} | ssh '{host.ssh}' '{service.docker()} load'",
                    ],
                )
                if result.returncode != 0:
                    click.echo(red(f"Failed to deploy image {service} to {host.name}!"))
                    sys.exit(result.returncode)
                click.echo(green(f"Deployed image {image} to {host.name}"))


@cli.command(name="start")
@click.argument("service", type=str, required=True, callback=resolve_service)
@click.argument("hosts", type=str, nargs=-1, callback=resolve_hosts)
@click.option(
    "--deploy",
    is_flag=True,
    type=bool,
    default=False,
    help="Deploy image before starting",
)
@click.option(
    "--no-build",
    is_flag=True,
    type=bool,
    default=False,
    help="Don't build image before deploying if --deploy is set",
)
@click.option(
    "--no-stop",
    is_flag=True,
    type=bool,
    default=False,
    help="Don't stop old instances of the service before starting",
)
@click.pass_context
def start_cmd(
    ctx: click.Context,
    service: Service,
    hosts: list[Host],
    deploy: bool,
    no_build: bool,
    no_stop: bool,
) -> None:
    """Start SERVICE on HOSTS."""
    if deploy:
        ctx.invoke(deploy_cmd, service=service, hosts=hosts, no_build=no_build)
    if not no_stop:
        ctx.invoke(stop_cmd, service=service, hosts=hosts)
    for host in hosts:
        with service._with_host(host):
            result = subprocess.run(
                host._command_prefix + service._run_command,
                capture_output=service.detach(),
            )
        if result.returncode != 0:
            click.echo(red(f"Failed to start {service.name()} on {host.name}!"))
            if result.stderr:
                click.echo(result.stderr)
            sys.exit(result.returncode)
        click.echo(green(f"Started {service.name()} on {host.name}"))


@cli.command(name="stop")
@click.argument("service", type=str, required=True, callback=resolve_service)
@click.argument("hosts", type=str, nargs=-1, callback=resolve_hosts)
@pass_group
def stop_cmd(service: Service, hosts: list[Host], group: Group) -> None:
    """Stop SERVICE on HOSTS."""
    for host in hosts:
        with service._with_host(host):
            result = subprocess.run(
                host._command_prefix
                + [service.docker(), "inspect", service.container_name()],
                capture_output=True,
            )
            try:
                inspection: list[dict] = json.loads(result.stdout)
                needs_stop = (
                    len(inspection) > 0
                    and inspection[0].get("State", dict()).get("Status", "")
                    == "running"
                )
            except Exception as e:
                click.echo(
                    red(
                        f"Failed to inspect container {service.container_name()} on {host.name}!"
                    )
                )
                click.echo(e)
                if result.stderr:
                    click.echo(result.stderr)
                sys.exit(1)

            if not needs_stop:
                continue

            result = subprocess.run(
                host._command_prefix + service._stop_command, capture_output=True
            )
            if result.returncode == 0:
                click.echo(green(f"Stopped {service.name()} on {host.name}"))
            else:
                click.echo(red(f"Failed to stop {service.name()} on {host.name}!"))
                if result.stderr:
                    click.echo(result.stderr)
                sys.exit(1)


@click.command(name="logs")
@click.argument("service", type=str, required=True, callback=resolve_service)
@click.argument("host", type=str, required=True, callback=resolve_host)
@click.option(
    "--follow", "-f", is_flag=True, type=bool, default=False, help="Follow log output"
)
def logs_cmd(service: Service, host: Host, follow: bool) -> None:
    """Show logs for SERVICE on HOST."""
    with service._with_host(host):
        docker_command = [
            service.docker(),
            "logs",
            *(["-f"] if follow else []),
            service.container_name(),
        ]
    result = subprocess.run(host._command_prefix + docker_command)
    if result.returncode != 0:
        click.echo(red(f"Failed to show logs for {service.name()} on {host.name}!"))
        sys.exit(result.returncode)


cli = CliWrapper(cli)
