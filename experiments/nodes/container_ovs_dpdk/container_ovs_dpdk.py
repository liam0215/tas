import threading

from components.container import Container
from nodes.node import Node


class ContainerOVSDPDK(Node):
    def __init__(
        self,
        defaults,
        machine_config,
        container_configs,
        wmanager,
        setup_pane_name,
        cleanup_pane_name,
        interface,
        pci_id,
        bridge_name="br-int",
    ):
        Node.__init__(
            self, defaults, machine_config, wmanager, setup_pane_name, cleanup_pane_name
        )

        self.container_configs = container_configs
        self.containers = []
        self.interface = interface
        self.pci_id = pci_id
        self.bridge_name = bridge_name
        self.script_dir = container_configs[0].manager_dir
        self.veth_base_name = "veth"

    def setup(self, is_client=False):
        super().setup()
        self.ovs_make_install(self.defaults.original_ovs_path)
        self.start_ovsdpdk(self.script_dir)
        self.ovsbr_add_internal(self.bridge_name, self.script_dir)

        for container_config in self.container_configs:
            veth_name_bridge = "{}{}".format(
                self.veth_base_name, (container_config.id * 2) + 1
            )
            veth_name_container = "{}{}".format(
                self.veth_base_name, container_config.id * 2)
            self.ovsveth_add(
                self.bridge_name,
                veth_name_bridge,
                veth_name_container,
                container_config.manager_dir,
                container_config.name,
                container_config.veth_bridge_ip,
                container_config.veth_container_ip,
                container_config.n_queues,
            )

        self.ovsbr_add_port(self.bridge_name, self.machine_config.interface)
        self.set_dpdk_interface(self.interface, self.pci_id, self.container_configs[0].n_queues)
        self.add_ip(self.bridge_name, self.machine_config.ip + "/24")
        self.interface_up(self.bridge_name)

    def cleanup(self):
        super().cleanup()
        self.ovsbr_del(self.bridge_name)
        self.stop_ovsdpdk(self.script_dir)
        self.add_ip_in_pane(self.cleanup_pane, self.interface,
                            self.machine_config.ip + "/24")
        self.interface_up_in_pane(self.cleanup_pane, self.interface)

        for container in self.containers:
            container.shutdown()
            container_config = container.container_config
            veth_name_bridge = "{}{}".format(
                self.veth_base_name, (container_config.id * 2) + 1
            )
            self.interface_del(veth_name_bridge)
            veth_name_container = "{}{}".format(
                self.veth_base_name, container_config.id * 2)
            self.interface_del(veth_name_container)

    def start_containers(self):
        threads = []
        for container_config in self.container_configs:
            container = Container(
                self.defaults,
                self.machine_config,
                container_config,
                self.wmanager
            )
            self.containers.append(container)
            container_thread = threading.Thread(target=container.start)
            threads.append(container_thread)
            container_thread.start()

        for t in threads:
            t.join()
