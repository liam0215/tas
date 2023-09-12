from configs.gen_config import Defaults
from configs.gen_config import MachineConfig
from configs.gen_config import TasConfig
from configs.gen_config import ContainerConfig
from configs.gen_config import ClientConfig
from configs.gen_config import ServerConfig


class Config:
    def __init__(self, exp_name, msize):
        self.exp_name = exp_name
        self.defaults = Defaults()

        self.tunnel = True
        # Server Machine
        self.sstack = 'container-virtuoso'
        self.snum = 1
        self.snodenum = 1
        self.s_container_configs = []
        self.s_tas_configs = []
        self.server_configs = []

        self.s_machine_config = MachineConfig(ip=self.defaults.server_ip,
                                              interface=self.defaults.server_interface,
                                              stack=self.sstack,
                                              is_remote=True,
                                              is_server=True)

        container0_config = ContainerConfig(pane=self.defaults.s_container_pane,
                                            machine_config=self.s_machine_config,
                                            vtas_dir=self.defaults.default_vtas_dir_bare,
                                            vtas_dir_virt=self.defaults.default_vtas_dir_virt,
                                            tas_dir=self.defaults.default_vtas_dir_bare,
                                            idx=0,
                                            n_cores=11,
                                            memory=10,
                                            tunnel=self.tunnel)
        tas_config = TasConfig(pane=self.defaults.s_tas_pane,
                               machine_config=self.s_machine_config,
                               project_dir=self.defaults.default_vtas_dir_bare,
                               ip=self.s_machine_config.ip,
                               n_cores=10, dpdk_extra="86:00.0")
        tas_config.args = tas_config.args + " --vm-shm-len=4294967296"

        self.s_container_configs.append(container0_config)
        self.s_tas_configs.append(tas_config)

        server0_config = ServerConfig(pane=self.defaults.s_server_pane,
                                      idx=0, vmid=0,
                                      port=1234, ncores=10, max_flows=4096, max_bytes=4096,
                                      bench_dir=self.defaults.default_vbenchmark_dir_virt,
                                      tas_dir=self.defaults.default_vtas_dir_virt)
        self.server_configs.append(server0_config)

        # Client Machine
        self.cstack = 'container-virtuoso'
        self.cnum = 1
        self.cnodenum = 1
        self.c_container_configs = []
        self.c_tas_configs = []
        self.client_configs = []

        self.c_machine_config = MachineConfig(ip=self.defaults.client_ip,
                                              interface=self.defaults.client_interface,
                                              stack=self.cstack,
                                              is_remote=False,
                                              is_server=False)

        container0_config = ContainerConfig(pane=self.defaults.c_container_pane,
                                            machine_config=self.c_machine_config,
                                            vtas_dir=self.defaults.default_vtas_dir_bare,
                                            vtas_dir_virt=self.defaults.default_vtas_dir_virt,
                                            tas_dir=self.defaults.default_vtas_dir_bare,
                                            idx=0,
                                            n_cores=11,
                                            memory=10,
                                            tunnel=self.tunnel)
        tas_config = TasConfig(pane=self.defaults.c_tas_pane,
                machine_config=self.c_machine_config,
                project_dir=self.defaults.default_vtas_dir_bare,
                ip=self.c_machine_config.ip,
                n_cores=10, dpdk_extra="d8:00.0")
        tas_config.args = tas_config.args + " --vm-shm-len=4294967296"

        self.c_container_configs.append(container0_config)
        self.c_tas_configs.append(tas_config)

        # TODO: Fix IP
        client0_config = ClientConfig(exp_name=exp_name,
                                      pane=self.defaults.c_client_pane,
                                      idx=0, vmid=0, stack=self.cstack,
                                      ip=self.defaults.server_ip, port=1234, ncores=10,
                                      msize=msize, mpending=64, nconns=1000,
                                      open_delay=3, max_msgs_conn=0, max_pend_conns=1,
                                      bench_dir=self.defaults.default_vbenchmark_dir_virt,
                                      tas_dir=self.defaults.default_vtas_dir_virt)

        self.client_configs.append(client0_config)
