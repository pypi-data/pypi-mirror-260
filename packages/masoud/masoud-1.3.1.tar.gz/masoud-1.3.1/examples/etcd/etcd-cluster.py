#!/usr/bin/env python3

import masoud


class Etcd(masoud.Service):
    def name(self) -> str:
        return "etcd"

    def image(self) -> str:
        return "github.com/satoqz/etcd"

    def dockerfile(self) -> tuple[str, str]:
        return ("examples/etcd/Dockerfile", ".")

    DEFAULT_CLIENT_PORT = 2379
    DEFAULT_PEER_PORT = 2380

    def ports(self) -> list[tuple[int, int]]:
        client_port = (
            self.host.get_var("etcd_client_port", int) or self.DEFAULT_CLIENT_PORT
        )
        peer_port = self.host.get_var("etcd_peer_port", int) or self.DEFAULT_PEER_PORT
        return [
            (client_port, self.DEFAULT_CLIENT_PORT),
            (peer_port, self.DEFAULT_PEER_PORT),
        ]

    DEFAULT_VOLUME_NAME = "example-etcd-data"
    VOLUME_MOUNT = "/data"

    def volumes(self) -> list[tuple[str, str]]:
        volume_name = self.host.get_var("etcd_volume", str) or self.DEFAULT_VOLUME_NAME
        return [(volume_name, self.VOLUME_MOUNT)]

    DEFAULT_INITIAL_CLUSTER_TOKEN = "example-etcd-cluster"

    def command(self) -> list[str]:
        ip = self.host.must_get_var("ip", str)
        client_port = (
            self.host.get_var("etcd_client_port", int) or self.DEFAULT_CLIENT_PORT
        )

        initial_cluster_token = (
            self.host.get_var("etcd_initial_cluster_token", str)
            or self.DEFAULT_INITIAL_CLUSTER_TOKEN
        )

        etcd_cluster_string = ",".join(
            f"{host.name}=http://{host.must_get_var("ip", str)}:{host.get_var("etcd_peer_port") or self.DEFAULT_PEER_PORT}"
            for host in self.group.get_hosts()
        )

        return [
            "etcd",
            f"--name={self.host.name}",
            f"--data-dir={self.VOLUME_MOUNT}/data",
            f"--wal-dir={self.VOLUME_MOUNT}/wal",
            f"--initial-advertise-peer-urls=http://{ip}:{self.DEFAULT_PEER_PORT}",
            f"--listen-peer-urls=http://0.0.0.0:{self.DEFAULT_PEER_PORT}",
            f"--listen-client-urls=http://0.0.0.0:{self.DEFAULT_CLIENT_PORT}",
            f"--advertise-client-urls=http://{ip}:{client_port}",
            f"--initial-cluster-token={initial_cluster_token}",
            f"--initial-cluster={etcd_cluster_string}",
            "--initial-cluster-state=new",
        ]


if __name__ == "__main__":
    masoud.cli(services=[Etcd()])
