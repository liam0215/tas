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
    self.vms = []
