import json
import subprocess
import sys
from collections.abc import Callable
from functools import update_wrapper

import click

from ._inventory import Inventory, Group, Host
from ._logging import err, ok
from ._service import Service


class CliWrapper(click.Group):
    def __init__(self, cli: click.Group) -> None:
        super().__init__(None, cli.commands)
        self.params = cli.params
        self.callback = cli.callback

    def __call__(self, services: list[Service], *args, **kwargs):
        return super().__call__(*args, **kwargs, obj={"services": services})


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
        err(f'host "{value}"" does not exist in group "{group.name}"')
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
            err(f'host "{value}" does not exist in group "{group.name}"')
            sys.exit(1)
        hosts.append(host)
    return hosts


def resolve_service(ctx: click.Context, _param: str, value: str) -> Service:
    services: list[Service] = ctx.obj["services"]
    group: Group = ctx.obj["group"]
    for service in services:
        with service._with_group(group):
            if service.name() == value:
                return service
    err(f'service "{value}" does not exist.')
    sys.exit(1)


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
@click.option("--debug", is_flag=True, type=bool, default=False)
@click.pass_context
def cli(ctx: click.Context, inventory: str, group: str | None, debug: bool) -> None:
    try:
        inv = Inventory(inventory, debug=debug)
    except Exception as e:
        err("could not read inventory!", e)
        sys.exit(1)

    group = group or inv.get_var("default_group", str)
    if group is not None:
        grp = inv.get_group(group)
        if grp is None:
            err(f'could not find group "{group}" in inventory')
            sys.exit(1)
    elif len(groups := inv.get_groups()) == 1:
        grp = groups[0]
    else:
        err(
            "no group (--group) given and no `default_group` inventory-level property set!"
        )
        sys.exit(1)

    ctx.obj["inventory"] = inv
    ctx.obj["group"] = grp


@cli.command(name="build")
@click.argument("service", type=str, required=True, callback=resolve_service)
@pass_group
def build_cmd(service: Service, group: Group) -> None:
    """Build the docker image for SERVICE, if needed."""
    with service._with_group(group):
        if service.dockerfile() is None:
            return
        result = group.localhost().run(service._build_command())
    if result.returncode != 0:
        sys.exit(1)


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
@pass_group
def deploy_cmd(
    ctx: click.Context,
    service: Service,
    hosts: list[Host],
    no_build: bool,
    group: Group,
) -> None:
    """Deploy SERVICE on HOSTS.
    This involves either building using the service's Dockerfile and copying it to the hosts
    or pulling the pre-built image on the hosts directly."""
    if not no_build:
        ctx.invoke(build_cmd, service=service)

    localhost = group.localhost()
    with service._with_host(localhost):
        dockerfile = service.dockerfile()
    with service._with_group(group):
        image = service.image()

    for host in hosts:
        with service._with_host(host):
            if dockerfile is None:
                result = host.run(service._pull_command())
                if result.returncode != 0:
                    err(f'failed to pull image "{image}" on "{host.name}"!')
                    sys.exit(1)
                ok(f'pulled image "{image}" on "{host.name}"')
                continue

            with service._with_host(localhost):
                export = localhost.popen(
                    service._docker() + ["save", image],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
            result = host.run(
                service._docker() + ["load"],
                text=True,
                capture_output=True,
                stdin=export.stdout,
            )
            export_returncode = export.wait()
            if result.returncode + export_returncode != 0:
                err(
                    f'failed to deploy image {service.name()} to "{host.name}"!',
                    export.stderr.read()
                    if export_returncode != 0 and export.stderr is not None
                    else None,
                    result.stderr if export.returncode != 0 else None,
                )
                sys.exit(1)
            ok(f'deployed image {image} to "{host.name}"')


@cli.command(name="start")
@click.argument("service", type=str, required=True, callback=resolve_service)
@click.argument("hosts", type=str, nargs=-1, callback=resolve_hosts)
@click.option(
    "--deploy",
    is_flag=True,
    type=bool,
    default=False,
    help="Deploy image before running",
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
@click.option(
    "--no-rm",
    is_flag=True,
    type=bool,
    default=False,
    help="Don't remove containers after stopping them",
)
@click.pass_context
def start_cmd(
    ctx: click.Context,
    service: Service,
    hosts: list[Host],
    deploy: bool,
    no_build: bool,
    no_stop: bool,
    no_rm: bool,
) -> None:
    """Start SERVICE on HOSTS."""
    if deploy:
        ctx.invoke(deploy_cmd, service=service, hosts=hosts, no_build=no_build)
    if not no_stop:
        ctx.invoke(stop_cmd, service=service, hosts=hosts, no_rm=no_rm)
    for host in hosts:
        with service._with_host(host):
            detach = service.detach()
            result = host.run(
                service._run_command(),
                text=detach,
                capture_output=detach,
            )
        if result.returncode != 0:
            err(f'failed to start "{service.name()}" on "{host.name}"!', result.stderr)
            sys.exit(1)
        ok(f'started "{service.name()}" on "{host.name}"')


@cli.command(name="stop")
@click.argument("service", type=str, required=True, callback=resolve_service)
@click.argument("hosts", type=str, nargs=-1, callback=resolve_hosts)
@click.option(
    "--no-rm",
    is_flag=True,
    type=bool,
    default=False,
    help="Don't remove containers after stopping them",
)
@click.pass_context
def stop_cmd(
    ctx: click.Context, service: Service, hosts: list[Host], no_rm: bool
) -> None:
    """Stop SERVICE on HOSTS."""
    for host in hosts:
        with service._with_host(host):
            result = host.run(
                service._docker() + ["inspect", service.container_name()],
                capture_output=True,
            )
            try:
                inspection: list[dict] = json.loads(result.stdout)
            except Exception as e:
                err(
                    f'failed to inspect container "{service.container_name()}" on "{host.name}"!',
                    e,
                    result.stderr,
                )
                sys.exit(1)

            running = (
                len(inspection) > 0
                and "State" in inspection[0]
                and isinstance(inspection[0]["State"], dict)
                and inspection[0]["State"]["Status"] == "running"
            )

            if not running:
                continue

            result = host.run(service._stop_command(), capture_output=True, text=True)
            if result.returncode != 0:
                err(
                    f'failed to stop "{service.name()}" on "{host.name}"!',
                    result.stderr,
                )
                sys.exit(1)
            ok(f'stopped "{service.name()}" on "{host.name}"')

    if not no_rm:
        ctx.invoke(rm_cmd, service=service, hosts=hosts)


@cli.command("rm")
@click.argument("service", type=str, required=True, callback=resolve_service)
@click.argument("hosts", type=str, nargs=-1, callback=resolve_hosts)
def rm_cmd(service: Service, hosts: list[Host]) -> None:
    """Remove leftover stopped containers for SERVICE on HOSTS."""
    for host in hosts:
        with service._with_host(host):
            docker, container_name = service._docker(), service.container_name()

            result = host.run(
                docker + ["inspect", container_name],
                capture_output=True,
            )
            try:
                inspection: list[dict] = json.loads(result.stdout)
            except Exception as e:
                err(
                    f'failed to inspect container "{service.container_name()}" on "{host.name}"!',
                    e,
                    result.stderr,
                )
                sys.exit(1)

            if len(inspection) < 1:
                continue

            result = host.run(
                docker + ["rm", container_name], text=True, capture_output=True
            )
            if result.returncode != 0:
                err(
                    f'failed to remove container "{container_name}" on "{host.name}"',
                    result.stderr,
                )
                sys.exit(1)
            ok(f'removed container "{container_name}" on "{host.name}"')


@cli.command(name="logs")
@click.argument("service", type=str, required=True, callback=resolve_service)
@click.argument("host", type=str, required=True, callback=resolve_host)
@click.option(
    "--follow", "-f", is_flag=True, type=bool, default=False, help="Follow log output"
)
def logs_cmd(service: Service, host: Host, follow: bool) -> None:
    """Show logs for SERVICE on HOST."""
    with service._with_host(host):
        docker_command = service._docker() + [
            "logs",
            *(["-f"] if follow else []),
            service.container_name(),
        ]
    result = host.run(docker_command)
    if result.returncode != 0:
        err(f'Failed to show logs for "{service.name()}" on "{host.name}"!')
        sys.exit(1)


@cli.command(name="status")
@click.argument("service", type=str, required=True, callback=resolve_service)
@click.argument("hosts", type=str, nargs=-1, callback=resolve_hosts)
def status_cmd(service: Service, hosts: list[Host]) -> None:
    """Check status for SERVICE on HOSTS."""
    for host in hosts:
        with service._with_host(host):
            result = host.run(
                service._docker() + ["inspect", service.container_name()],
                capture_output=True,
            )
            try:
                inspection: list[dict] = json.loads(result.stdout)
            except Exception as e:
                err(
                    f'failed to inspect container "{service.container_name()}" on "{host.name}"!',
                    e,
                    result.stderr,
                )
                sys.exit(1)

            running = (
                len(inspection) > 0
                and "State" in inspection[0]
                and isinstance(inspection[0]["State"], dict)
                and inspection[0]["State"]["Status"] == "running"
            )

            if running:
                ok(f'"{service.name()}" is up on "{host.name}"')
            else:
                err(f'{service.name()} is down on "{host.name}"')


cli = CliWrapper(cli)
