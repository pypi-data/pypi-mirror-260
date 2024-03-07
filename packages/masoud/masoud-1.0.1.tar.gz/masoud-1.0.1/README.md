# Masoud

> *Masoud (Arabic: مسعود يُقرأ:مَس عُود, lit. 'fortune, happy, prosperous, lucky'*

- [Installation](#installation)
- [Usage](#service-definitions)
- [Service API](#service-api)

Here's what I needed and why I created Masoud:

- I needed to deploy several containers to several hosts from a single control plane
- I needed a configuration format more dynamic that Docker Compose
- I didn't need a complex general-purpose server-management tool like Ansible or NixOS
- I didn't need a complex orchestrator like Kubernetes

If you find yourself in the same situation, Masoud is for you!

## Installation

Masoud is available on [PyPI](https://pypi.org/project/masoud/).

## Usage

First, define your `inventory.toml`:

```toml
default_group = "my-group"

[my-group.hosts]
my-host = { ssh = "my-user@my-host", nginx_port = 3000 }
```

Below is the obligatory example for a minimal Nginx service:

```python
class Nginx(masoud.Service):
    def name(self) -> str:
        return "nginx"
    
    def image(self) -> str:
        return "docker.io/nginx:latest"
    
    def ports(self) -> list[tuple[int, int]]:
        external_port = self.host.get_var("nginx_port", int) or 8080
        return [(external_port, 80)]
```

> (For a more sophisticated example, see [examples/etcd/etcd-cluster.py](./examples/etcd/etcd-cluster.py)).

You can then create a CLI to manage your Nginx service:

`nginx-cli.py`
```python
masoud.cli(services=[Nginx()])
```

Now deploy and start the service on your host:

```sh
python3 nginx-cli.py start nginx my-host --deploy
```

The following are all commands available for service/host management:

```sh
Usage:  [OPTIONS] COMMAND [ARGS]...

Options:
  -i, --inventory TEXT  Path to the inventory TOML file (default:
                        inventory.toml)
  -g, --group TEXT      Inventory group to operate on, default is set through
                        `default_group` key
  --help                Show this message and exit.

Commands:
  build   Build the docker image for SERVICE, if needed.
  deploy  Deploy SERVICE on HOSTS.
  ssh     Connect to HOST via SSH.
  start   Start SERVICE on HOSTS.
  stop    Stop SERVICE on HOSTS.
```

Additionally, the [`click`](https://click.palletsprojects.com/) CLI used by Masoud is exposed as `masoud.cli`. This lets you add your own commands to the CLI for convenience:

```python
@masoud.cli.command
def hello() -> None:
    print("Hello, World!")
```

## Service API

You can override the following methods on `masoud.Service` to customize your service. The minimum required overrides are `name` and `image`.

```python
def command(self) -> list[str]:
    """The command that is passed to the container"""

def container_name(self) -> str:
    """Container name"""

def detach(self) -> bool:
    """Pass the `-d/--detach` flag to `docker run`"""

def do_rm(self) -> bool:
    """Pass the `--rm` flag to `docker run`"""

def docker(self) -> str:
    """The name/path of the docker command"""

def dockerfile(self) -> tuple[str, str] | None:
    """Path to the Dockerfile that builds the service's image.
        Keep this empty to pull the image from a registry instead."""

def extra_build_args(self) -> list[str]:
    """Additional arguments passed to `docker build`"""

def extra_pull_args(self) -> list[str]:
    """Additional arguments passed to `docker pull`"""

def extra_run_args(self) -> list[str]:
    """Additional arguments passed to `docker run`"""

def image(self) -> str:
    """The tag of the docker image used by the service"""

def name(self) -> str:
    """The name of the service"""

def needs_init(self) -> bool:
    """Pass the `--init` flag to `docker run`"""

def ports(self) -> list[tuple[int | str, int | str]]:
    """List of `(outer_port, inner_port)` mappings"""

def stop_signal(self) -> str | None:
    """Signal passed to `-s` argument of `docker stop`"""

def stop_timeout(self) -> int | None:
    """Timeout passed to `-t` argument of `docker stop`"""

def volumes(self) -> list[tuple[str, str] | tuple[str, str, str]]:
    """List of `(volume, mountpoint, [options])` mappings"""
```
