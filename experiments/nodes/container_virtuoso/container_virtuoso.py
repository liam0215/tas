import time
import threading

from components.tas import TAS
from components.container import Container
from nodes.node import Node


class ContainerVirtuoso(Node):
    def __init__(
        self,
        defaults,
        machine_config,
        container_configs,
        tas_configs,
        wmanager,
        setup_pane_name,
        cleanup_pane_name,
        interface,
        pci_id,
    ):
        Node.__init__(
            self, defaults, machine_config, wmanager, setup_pane_name, cleanup_pane_name
        )

        self.container_configs = container_configs
        self.containers = []
        self.tas_configs = tas_configs
        self.tas = []
        self.interface = interface
        self.pci_id = pci_id
        self.script_dir = container_configs[0].manager_dir

    def cleanup(self):
        super().cleanup()
        for tas in self.tas:
            tas.cleanup(self.cleanup_pane)

        for container in self.containers:
            container.shutdown()

    def start_tas(self):
        for i in range(self.nodenum):
            tas_config = self.tas_configs[i]

            tas = TAS(defaults=self.defaults,
                      machine_config=self.machine_config,
                      tas_config=tas_config,
                      vm_config=self.container_configs[i],
                      wmanager=self.wmanager)

            self.tas.append(tas)
            tas.run_bare()
            time.sleep(3)

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
