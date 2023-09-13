import time

from nodes.container_ovs_dpdk.container_ovs_dpdk import ContainerOVSDPDK
from components.client import Client

class ContainerOVSDPDKClient(ContainerOVSDPDK):
  
  def __init__(self, config, wmanager):

    ContainerOVSDPDK.__init__(self, config.defaults, config.c_cset_configs,
                              config.c_machine_config,
                              config.c_container_configs,
                              wmanager,
                              config.defaults.c_setup_pane,
                              config.defaults.c_cleanup_pane,
                              config.defaults.server_interface,
                              config.defaults.server_interface_pci,
                              )

    self.client_configs = config.client_configs
    self.nodenum = config.cnodenum
    self.cnum = config.cnum
    self.clients = []

  def cleanup(self):
    super().cleanup()

  def start_clients(self):
    for i in range(self.nodenum):
      container_config = self.container_configs[i]
      for j in range(self.cnum):
        cidx = self.cnum * i + j
        client_config = self.client_configs[cidx]
        client = Client(self.defaults, 
            self.machine_config,
            client_config, 
            container_config, 
            self.wmanager)
        self.clients.append(client)
        client.run_virt(False, False)
        time.sleep(3)

  def run(self):
    self.start_containers()
    self.setup(is_client=True)
    self.start_clients()

  def save_logs(self, exp_path):
    for client in self.clients:
      client.save_log_virt(exp_path)
