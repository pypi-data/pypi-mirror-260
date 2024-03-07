from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import cast, Iterator

from ._inventory import Inventory, Group, Host


class Service(ABC):
    @abstractmethod
    def name(self) -> str:
        """The name of the service"""
        ...

    @abstractmethod
    def image(self) -> str:
        """The tag of the docker image used by the service"""
        ...

    def docker(self) -> str:
        """The name/path of the docker command"""
        return "docker"

    def extra_pull_args(self) -> list[str]:
        """Additional arguments passed to `docker pull`"""
        return []

    def dockerfile(self) -> tuple[str, str] | None:
        """Path to the Dockerfile that builds the service's image.
        Keep this empty to pull the image from a registry instead."""
        return None

    def extra_build_args(self) -> list[str]:
        """Additional arguments passed to `docker build`"""
        return []

    def do_rm(self) -> bool:
        """Pass the `--rm` flag to `docker run`"""
        return True

    def needs_init(self) -> bool:
        """Pass the `--init` flag to `docker run`"""
        return True

    def detach(self) -> bool:
        """Pass the `-d/--detach` flag to `docker run`"""
        return True

    def ports(self) -> list[tuple[int | str, int | str]]:
        """List of `(outer_port, inner_port)` mappings"""
        return []

    def volumes(self) -> list[tuple[str, str] | tuple[str, str, str]]:
        """List of `(volume, mountpoint, [options])` mappings"""
        return []

    def container_name(self) -> str:
        """Container name"""
        return self.name()

    def extra_run_args(self) -> list[str]:
        """Additional arguments passed to `docker run`"""
        return []

    def command(self) -> list[str]:
        """The command that is passed to the container"""
        return []

    def stop_signal(self) -> str | None:
        """Signal passed to `-s` argument of `docker stop`"""
        return None

    def stop_timeout(self) -> int | None:
        """Timeout passed to `-t` argument of `docker stop`"""
        return None

    @property
    def _pull_command(self) -> list[str]:
        return [self.docker(), "pull", *self.extra_pull_args(), self.image()]

    @property
    def _build_command(self) -> list[str]:
        dockerfile = self.dockerfile()
        if dockerfile is None:
            raise RuntimeError(
                "Trying to build container that has no dockerfile configured"
            )

        return [
            self.docker(),
            "build",
            f"-t={self.image()}",
            f"-f={dockerfile[0]}",
            *self.extra_build_args(),
            dockerfile[1],
        ]

    @property
    def _run_command(self) -> list[str]:
        return (
            [
                self.docker(),
                "run",
                *(["--rm"] if self.do_rm() else []),
                *(["--init"] if self.needs_init() else []),
                *(["-d"] if self.detach() else []),
                f"--name={self.container_name()}",
            ]
            + [
                f'-p="{outer_port}:{inner_port}"'
                for outer_port, inner_port in self.ports()
            ]
            + [
                f'-v={volume[0]}:{volume[1]}{f":{cast(tuple[str, str, str], volume)[2]}" if len(volume) > 2 else ""}'
                for volume in self.volumes()
            ]
            + self.extra_run_args()
            + [self.image()]
            + self.command()
        )

    @property
    def _stop_command(self) -> list[str]:
        return [
            self.docker(),
            "stop",
            *([f"-s={signal}"] if (signal := self.stop_signal()) is not None else []),
            *(
                [f"-t={timeout}"]
                if (timeout := self.stop_timeout()) is not None
                else []
            ),
            self.container_name(),
        ]

    _host: Host | None
    _group: Group | None
    _inventory: Inventory | None

    @contextmanager
    def _with_host(self, host: Host) -> Iterator[None]:
        self._host = host
        self._group = host.group
        self._inventory = host.group.inventory
        yield
        self._host, self._group, self._inventory = None, None, None

    @property
    def host(self) -> Host:
        """Reference to the host the service is being used with.
        Not available during builds, since they are host-agnostic.
        You can however access `self.group` during builds."""
        if self._host is None:
            raise RuntimeError("`self.host` is not available in this phase")
        return self._host

    @contextmanager
    def _with_group(self, group: Group) -> Iterator[None]:
        self._group, self._inventory = group, group.inventory
        yield
        self._group, self._inventory = None, None

    @property
    def group(self) -> Group:
        """Reference to the inventory group the service is being used with"""
        if self._group is None:
            raise RuntimeError(
                "INTERNAL ERROR: `self.group` was accessed outside of `_with_group` or `_with_host` context"
            )
        return self._group

    @property
    def inventory(self) -> Inventory:
        """Reference to the inventory the service is being used with"""
        if self.inventory is None:
            raise RuntimeError(
                "INTERNAL ERROR: `self.inventory` was accessed outside of `_with_group` or `_with_host` context"
            )
        return self.inventory
