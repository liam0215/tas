import time
from nodes.node import Node


class BareTas(Node):

    def __init__(self, defaults, machine_config, tas_config, cset_configs,
                 wmanager, setup_pane_name, cleanup_pane_name):

        Node.__init__(self, defaults, machine_config, cset_configs, wmanager,
                      setup_pane_name, cleanup_pane_name)

        self.tas_config = tas_config

    def cleanup(self):
        super().cleanup()
        remove_tas_socket_com = "find {} -name \"*flexnic_os*\" | xargs rm -r".format(
            self.tas_config.project_dir)
        self.cleanup_pane.send_keys(remove_tas_socket_com)
