import time

from nodes.container_ovs_dpdk.container_ovs_dpdk import ContainerOVSDPDK
from components.server import Server


class ContainerOVSDPDKServer(ContainerOVSDPDK):

    def __init__(self, config, wmanager):

        ContainerOVSDPDK.__init__(self, config.defaults, config.s_cset_configs, 
                                  config.s_machine_config,
                                  config.s_container_configs,
                                  wmanager,
                                  config.defaults.s_setup_pane,
                                  config.defaults.s_cleanup_pane,
                                  config.defaults.server_interface,
                                  config.defaults.server_interface_pci,
                                  )

        self.server_configs = config.server_configs
        self.nodenum = config.snodenum
        self.snum = config.snum

    def start_servers(self):
        for i in range(self.nodenum):
            container_config = self.container_configs[i]
            for j in range(self.snum):
                sidx = self.snum * i + j
                server_config = self.server_configs[sidx]
                server = Server(self.defaults,
                                self.machine_config,
                                server_config,
                                container_config,
                                self.wmanager)
                server.run_virt(False, False)
                time.sleep(3)

    def run(self):
        self.start_containers()
        self.setup()
        self.start_servers()
