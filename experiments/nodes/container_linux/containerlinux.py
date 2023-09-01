import time
import threading

from components.container import Container
from nodes.node import Node

class ContainerLinux(Node):
  
  def __init__(self, defaults, machine_config,
      container_configs, wmanager, 
      setup_pane_name, cleanup_pane_name):

    Node.__init__(self, defaults, machine_config, wmanager, 
        setup_pane_name, cleanup_pane_name)
        
    self.container_configs = container_configs
    self.containers = []

  def setup(self, is_client=False):
    super().setup()
    self.ovs_make_install(self.defaults.original_ovs_path)
    script_dir = self.container_configs[0].manager_dir
    self.start_ovsdpdk(script_dir)
    self.ovsbr_add_internal("br-int", script_dir)

    if is_client:
      remote_ip = self.defaults.server_ip
      mac = self.defaults.client_mac
    else:
      remote_ip = self.defaults.client_ip
      mac = self.defaults.server_mac
    
    for container_config in self.container_configs:
      veth_name_bridge = "veth{}".format((container_config.id * 2) + 1)
      veth_name_container = "veth{}".format(container_config.id * 2)
      self.ovsveth_add("br-int", veth_name_bridge, veth_name_container, 
                       container_config.manager_dir, container_config.name,
                       container_config.veth_bridge_ip, 
                       container_config.veth_container_ip,
                       container_config.n_queues)
