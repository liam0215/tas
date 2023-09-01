import time

class Container:
    def __init__(self, defaults, machine_config, container_config, wmanager):
        self.defaults = defaults
        self.machine_config = machine_config
        self.container_config = container_config
        self.wmanager = wmanager
        self.pane = self.wmanager.add_new_pane(container_config.pane,
                machine_config.is_remote)
    
    def start(self):
        self.pane.send_keys('cd ' + self.container_config.manager_dir)
        start_container_cmd = "sudo bash start-container.sh {} {} {} {} {}".format(
            self.machine_config.stack, self.container_config.id,
            self.container_config.n_cores, self.container_config.memory,
            self.container_config.name)
        self.pane.send_keys(start_container_cmd)

        print("Started Container")
        time.sleep(5)
        # What do after vm is up?