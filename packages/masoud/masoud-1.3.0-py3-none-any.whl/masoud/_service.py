from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import cast, Iterator

from ._inventory import Inventory, Group, Host


class Service(ABC):
    """A service describes how a certain docker container is built/run/stopped/...
    within the context of its host, group and inventory.
    """

    _host: Host | None = None
    _group: Group | None = None
    _inventory: Inventory | None = None

    @contextmanager
    def _with_host(self, host: Host) -> Iterator[None]:
        prev_host, prev_group, prev_inventory = self._host, self._group, self._inventory
        self._host, self._group, self._inventory = host, host.group, host.inventory
        yield
        self._host, self._group, self._inventory = prev_host, prev_group, prev_inventory

    @property
    def host(self) -> Host:
        """Reference to the host the service is being used with.
        Not guaranteed to be available when evaluating `self.name` or `self.image`.
        This will be `localhost` during builds.
        """
        if self._host is None:
            raise RuntimeError("`self.host` is not available in this phase")
        return self._host

    @contextmanager
    def _with_group(self, group: Group) -> Iterator[None]:
        prev_group, prev_inventory = self._group, self._inventory
        self._group, self._inventory = group, group.inventory
        yield
        self._group, self._inventory = prev_group, prev_inventory

    @property
    def group(self) -> Group:
        """Reference to the inventory group the service is being used with"""
        if self._group is None:
            raise RuntimeError("`self.group` is not available in this phase.")
        return self._group

    @property
    def inventory(self) -> Inventory:
        """Reference to the inventory the service is being used with"""
        if self.inventory is None:
            raise RuntimeError("`self.inventory` is not available in this phase")
        return self.inventory

    @abstractmethod
    def name(self) -> str:
        """The name of the service."""
        ...

    @abstractmethod
    def image(self) -> str:
        """The tag of the docker image used by the service."""
        ...

    def docker(self) -> str:
        """The name/path of the docker command, you can also put `podman` here!
        Default: `"docker".`
        """
        return "docker"

    def context(self) -> str | None:
        """The docker context to use, see `docker --context`.
        Default: `None`.
        """
        return None

    def extra_pull_args(self) -> list[str]:
        """Additional arguments passed to `docker pull`.
        Default: `[]`.
        """
        return []

    def dockerfile(self) -> tuple[str, str] | None:
        """Path to the Dockerfile that builds the service's image.
        Keep this empty to pull the image from a registry instead.
        Default: `None`.
        """
        return None

    def extra_build_args(self) -> list[str]:
        """Additional arguments passed to `docker build.`
        Default: `[]`.
        """
        return []

    def container_name(self) -> str:
        """Container name passed to see `docker run --name`.
        Default: `self.name()`.
        """
        return self.name()

    def do_rm(self) -> bool:
        """Pass the `--rm` flag to `docker run`. Conflicts with `restart`.
        Default: `False`.
        """
        return False

    def needs_init(self) -> bool:
        """Pass the `--init` flag to `docker run`.
        Default: `True`.
        """
        return True

    def detach(self) -> bool:
        """Pass the `-d/--detach` flag to `docker run`.
        Default: `True`.
        """
        return True

    def restart(self) -> str | None:
        """Restart option that is passed to `docker run --restart`.
        Default: `"unless-stopped"`"""
        return "unless-stopped"

    def ports(self) -> list[tuple[int | str, int | str]]:
        """List of `(outer_port, inner_port)` mappings passed to `docker run -p`.
        Default: `[]`.
        """
        return []

    def volumes(self) -> list[tuple[str, str] | tuple[str, str, str]]:
        """List of `(volume, mountpoint, [options])` mappings passed to `docker run -v`.
        Default: `[]`.
        """
        return []

    def networks(self) -> list[str]:
        """List of networks passed to `docker run --network`.
        Default: `[]`.
        """
        return []

    def extra_run_args(self) -> list[str]:
        """Additional arguments passed to `docker run`.
        Default: `[]`.
        """
        return []

    def command(self) -> list[str]:
        """The command that is passed to the container (at the end of the `docker run` command).
        Default: `[]`.
        """
        return []

    def stop_signal(self) -> str | None:
        """Signal passed to `-s` argument of `docker stop`.
        Default: `None`.
        """
        return None

    def stop_timeout(self) -> int | None:
        """Timeout passed to `-t` argument of `docker stop`.
        Default: `None`.
        """
        return None

    def _docker(self) -> list[str]:
        context = self.context()
        return [self.docker()] + ([context] if context is not None else [])

    def _pull_command(self) -> list[str]:
        return self._docker() + ["pull", *self.extra_pull_args(), self.image()]

    def _build_command(self) -> list[str]:
        dockerfile = self.dockerfile()
        if dockerfile is None:
            raise RuntimeError(
                "Trying to build container that has no dockerfile configured"
            )

        return self._docker() + [
            "build",
            f"-t={self.image()}",
            f"-f={dockerfile[0]}",
            *self.extra_build_args(),
            dockerfile[1],
        ]

    def _run_command(self) -> list[str]:
        return (
            self._docker()
            + [
                "run",
                f"--name={self.container_name()}",
                *(["--rm"] if self.do_rm() else []),
                *(["--init"] if self.needs_init() else []),
                *(["-d"] if self.detach() else []),
                *(
                    [f"--restart={restart}"]
                    if ((restart := self.restart()) not in [None, "no"])
                    else []
                ),
            ]
            + [
                f"-p={outer_port}:{inner_port}"
                for outer_port, inner_port in self.ports()
            ]
            + [
                f'-v={volume[0]}:{volume[1]}{f":{cast(tuple[str, str, str], volume)[2]}" if len(volume) > 2 else ""}'
                for volume in self.volumes()
            ]
            + [f"--network={network}" for network in self.networks()]
            + self.extra_run_args()
            + [self.image()]
            + self.command()
        )

    def _stop_command(self) -> list[str]:
        return self._docker() + [
            "stop",
            *([f"-s={signal}"] if (signal := self.stop_signal()) is not None else []),
            *(
                [f"-t={timeout}"]
                if (timeout := self.stop_timeout()) is not None
                else []
            ),
            self.container_name(),
        ]
