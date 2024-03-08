"""Masoud's inventory data structure based on TOML"""

from __future__ import annotations

import tomllib
import subprocess
from datetime import datetime
from typing import cast

from ._logging import debug

Toml = bool | int | float | str | datetime | list["Toml"] | dict[str, "Toml"]
"""Every possible TOML value type"""


class TomlContainer:
    """Wrapper around the dict returned by tomllib that ensures relatively type-safe access"""

    toml: dict[str, Toml]
    """The wrapped tomllib dict"""

    def __init__(self, toml: dict[str, Toml]) -> None:
        self.toml = toml

    def get_var[T: Toml](
        self, name: str, check_type: type[T] | None = None
    ) -> T | None:
        """Try to find a value in the TOML dict, optionally performing a type check"""
        var = self.toml.get(name, None)
        if var is None:
            return None
        if check_type is not None and not isinstance(var, check_type):
            raise ValueError(f"Expected {check_type} for TOML key {name} but got {var}")
        return cast(T, var)

    def must_get_var[T: Toml](self, name: str, check_type: type[T] | None = None) -> T:
        """Same as `get_var`, but raises if no value is found"""
        var = self.get_var(name, check_type)
        if var is None:
            raise ValueError(f"Cannot get variable {name}")
        return var


class Inventory(TomlContainer):
    """Representation of an inventory.toml file"""

    _groups: TomlContainer | None = None
    _debug: bool

    def __init__(self, path: str, debug: bool = False) -> None:
        self._debug = debug
        with open(path, "rb") as f:
            toml = tomllib.load(f)
            super().__init__(toml)
        groups_toml = self.get_var("groups", dict)
        if groups_toml is not None:
            self._groups = TomlContainer(groups_toml)

    def get_group(self, name: str) -> Group | None:
        """Try to find a group defined on the inventory"""
        toml = self.get_var(name, dict)
        if toml is None:
            return None
        return Group(name, self, toml)

    def get_groups(self) -> list[Group]:
        """Get all groups defined in the inventory"""
        ret = []
        if self._groups is None:
            return ret
        for key in self._groups.toml:
            group_toml = self._groups.get_var(key)
            if group_toml is None or not isinstance(group_toml, dict):
                continue
            ret.append(Group(key, self, group_toml))
        return ret


class Group(TomlContainer):
    """A group of hosts within the inventory"""

    name: str
    """Name of the group"""
    inventory: "Inventory"
    """Upwards-reference to the inventory the group is defined in"""
    _hosts: TomlContainer | None = None

    def __init__(
        self, name: str, inventory: "Inventory", toml: dict[str, Toml]
    ) -> None:
        super().__init__(toml)
        self.name = name
        self.inventory = inventory
        hosts_toml = self.get_var("hosts", dict)
        if hosts_toml is not None:
            self._hosts = TomlContainer(hosts_toml)

    def get_var[T: Toml](
        self, name: str, check_type: type[T] | None = None
    ) -> T | None:
        """Try to find a variable for the group, optionally performing a type check.
        If a variable is not defined on the host, it is retried "upwards" by trying to
        find it in the inventory root.
        """
        var = super().get_var(name, check_type)
        if var is not None:
            return var
        return self.inventory.get_var(name, check_type)

    def get_host(self, name: str) -> Host | None:
        """Try to find a host defined on the group"""
        if self._hosts is None:
            return None
        host_toml = self._hosts.get_var(name, dict)
        if host_toml is None:
            return None
        return Host(name, self, self.inventory, host_toml)

    def get_hosts(self) -> list[Host]:
        """Get all hosts defined on the group"""
        ret = []
        if self._hosts is None:
            return ret
        for key in self._hosts.toml:
            host_toml = self._hosts.get_var(key)
            if host_toml is None or not isinstance(host_toml, dict):
                continue
            ret.append(Host(key, self, self.inventory, host_toml))
        return ret

    def localhost(self) -> Host:
        """Get the always-defined `localhost` host"""
        user_defined = self.get_host("localhost")
        if user_defined is not None:
            return user_defined
        return Host("localhost", self, self.inventory, {})


class Host(TomlContainer):
    """A single host within the inventory"""

    name: str
    """Name of the host"""
    ssh: str
    """SSH connection string, empty if host is `localhost`"""
    group: "Group"
    """Upwards-reference to the group the host is defined in"""
    inventory: "Inventory"
    """Upwards-reference to the inventory the host is defined in"""

    def __init__(
        self, name: str, group: "Group", inventory: Inventory, toml: dict[str, Toml]
    ) -> None:
        super().__init__(toml)
        self.name = name
        self.group = group
        self.inventory = inventory

        ssh = super().get_var("ssh", str) or ""

        if ssh == "" and name != "localhost":
            raise ValueError(
                f'host "{name}" is missing `ssh` variable and isn\'t "localhost"'
            )
        elif ssh != "" and name == "localhost":
            raise ValueError('"localhost" must not have an `ssh` variable')

        self.ssh = ssh

    def get_var[T: Toml](
        self, name: str, check_type: type[T] | None = None
    ) -> T | None:
        """Try to find a variable for the host, optionally performing a type check.
        If a variable is not defined on the host, it is retried "upwards" by first
        trying to find it defined on the group and lastly trying to find it defined
        on the inventory root.
        """
        var = super().get_var(name, check_type)
        if var is not None:
            return var
        return self.group.get_var(name, check_type)

    @property
    def _command_prefix(self) -> list[str]:
        if self.ssh == "":
            return []
        return ["ssh", self.ssh]

    def popen(self, args: list[str], **kwargs) -> subprocess.Popen:
        """Open a process on the host"""
        cmd = self._command_prefix + args
        if self.inventory._debug:
            debug(" ".join(cmd))
        return subprocess.Popen(cmd, **kwargs)

    def run(
        self,
        args: list[str],
        **kwargs,
    ) -> subprocess.CompletedProcess[bytes]:
        """Run a command on the host"""
        cmd = self._command_prefix + args
        if self.inventory._debug:
            debug(" ".join(cmd))
        return subprocess.run(self._command_prefix + args, **kwargs)
