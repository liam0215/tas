import time

from nodes.container_virtuoso.container_virtuoso import ContainerVirtuoso
from components.server import Server


class ContainerVirtuosoServer(ContainerVirtuoso):

    def __init__(self, config, wmanager):

        ContainerVirtuoso.__init__(self, config.defaults, config.s_machine_config,
                                   config.s_container_configs,
                                   config.s_tas_configs,
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
                server.pane.send_keys(
                    "export TAS_GROUP={}".format(server_config.groupid))
                server.run_virt(True, True)
                server.pane.send_keys("tas")
                time.sleep(3)

    def run(self):
        self.setup()
        self.start_tas()
        self.start_containers()
        self.start_servers()
