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
$help
```

Additionally, the [`click`](https://click.palletsprojects.com/) CLI used by Masoud is exposed as `masoud.cli`. This lets you add your own commands to the CLI for convenience:

```python
@masoud.cli.command
def hello() -> None:
    print("Hello, World!")
```

## Service API

You can override the following methods on `masoud.Service` to customize your service. The minimum required overrides are `name` and `image`.

$api