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
        start_container_cmd = "sudo bash start-container.sh {} {} {} {} {} {}".format(
            self.machine_config.stack, self.container_config.id,
            self.container_config.n_cores, self.container_config.memory,
            self.container_config.name, self.container_config.tas_dir)
        self.pane.send_keys(start_container_cmd)

        print("Started Container")
        time.sleep(3)
        self.enter_container()

    def enter_container(self):
        enter_container_cmd = "sudo docker exec -it {} bash".format(
            self.container_config.name)
        self.pane.send_keys(enter_container_cmd)
        time.sleep(1)

    def shutdown(self):
        self.pane.send_keys(suppress_history=False, cmd='whoami')

        captured_pane = self.pane.capture_pane()
        user = captured_pane[len(captured_pane) - 2]

        # This means we are in the container, so we don't
        # accidentally exit machine
        if user == 'tas':
            self.pane.send_keys(suppress_history=False, cmd='exit')
            time.sleep(2)

        kill_container_cmd = "sudo docker container kill {}".format(
            self.container_config.name)
        self.pane.send_keys(kill_container_cmd)
        prune_container_cmd = "sudo docker container prune -f"
        self.pane.send_keys(prune_container_cmd)
