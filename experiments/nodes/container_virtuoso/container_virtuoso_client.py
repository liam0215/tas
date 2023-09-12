import time

from nodes.container_virtuoso.container_virtuoso import ContainerVirtuoso
from components.client import Client

class ContainerVirtuosoClient(ContainerVirtuoso):
  
  def __init__(self, config, wmanager):

    ContainerVirtuoso.__init__(self, config.defaults, config.c_machine_config,
                                config.c_container_configs,
                                config.c_tas_configs,
                                wmanager,
                                config.defaults.c_setup_pane,
                                config.defaults.c_cleanup_pane,
                                config.defaults.client_interface,
                                config.defaults.client_interface_pci,
                                )

    self.client_configs = config.client_configs
    self.nodenum = config.cnodenum
    self.cnum = config.cnum
    self.clients = []

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
        client.run_virt(True, True)
        client.pane.send_keys("tas")
        time.sleep(3)

  def run(self):
    self.setup()
    self.start_tas()
    self.start_containers()
    self.start_clients()

  def save_logs(self, exp_path):
    for client in self.clients:
      client.save_log_virt(exp_path)
