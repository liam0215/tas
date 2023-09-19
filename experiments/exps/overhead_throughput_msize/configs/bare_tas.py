from configs.gen_config import Defaults
from configs.gen_config import MachineConfig
from configs.gen_config import TasConfig
from configs.gen_config import ClientConfig
from configs.gen_config import ServerConfig
from configs.gen_config import CSetConfig

class Config:
    def __init__(self, exp_name, msize):
        self.exp_name = exp_name
        self.defaults = Defaults()
        
        # Configure csets
        self.s_cset_configs = []
        self.c_cset_configs = []
        tas_cset = CSetConfig([1,3,5,7,9,11], "0-1", "tas_server")
        self.s_cset_configs.append(tas_cset)
        tas_cset = CSetConfig([1,3,5,7,9,11], "0-1", "tas_client")
        self.c_cset_configs.append(tas_cset)

        vm0_cset = CSetConfig([19,21,23,25,27,29,31,33,35,37,39,41,43], "0-1", "server")
        self.s_cset_configs.append(vm0_cset)

        vm0_cset = CSetConfig([19,21,23,25,27,29,31,33,35,37,39,41,43], "0-1", "client")
        self.c_cset_configs.append(vm0_cset)

        # Server Machine
        self.sstack = 'bare-tas'
        self.snum = 1
        self.snodenum = 1
        self.s_tas_configs = []
        self.s_vm_configs = []
        self.s_proxyg_configs = []
        self.server_configs = []
        
        self.s_machine_config = MachineConfig(ip=self.defaults.server_ip, 
                interface=self.defaults.server_interface,
                stack=self.sstack,
                is_remote=True,
                is_server=True)

        tas_config = TasConfig(pane=self.defaults.s_tas_pane,
                machine_config=self.s_machine_config,
                project_dir=self.defaults.default_otas_dir_bare,
                ip=self.s_machine_config.ip,
                cset="tas_server",
                n_cores=5,
                pci="86:00.0",
                cores=tas_cset.cores)
        self.s_tas_configs.append(tas_config)

        server0_config = ServerConfig(pane=self.defaults.s_server_pane,
                idx=0, vmid=0,
                port=1234, ncores=12, max_flows=4096, max_bytes=4096,
                cset="server",
                bench_dir=self.defaults.default_obenchmark_dir_bare,
                tas_dir=self.defaults.default_otas_dir_bare,
                cores=vm0_cset.cores)
        self.server_configs.append(server0_config)

        # Client Machine
        self.cstack = 'bare-tas'
        self.cnum = 1
        self.cnodenum = 1
        self.c_tas_configs = []
        self.c_vm_configs = []
        self.c_proxyg_configs = []
        self.client_configs = []

        self.c_machine_config = MachineConfig(ip=self.defaults.client_ip, 
                interface=self.defaults.client_interface,
                stack=self.cstack,
                is_remote=False,
                is_server=False)

        tas_config = TasConfig(pane=self.defaults.c_tas_pane,
                machine_config=self.c_machine_config,
                project_dir=self.defaults.default_otas_dir_bare,
                ip=self.c_machine_config.ip,
                cset="tas_client",
                n_cores=5,
                cores=tas_cset.cores)
        self.c_tas_configs.append(tas_config)

        client0_config = ClientConfig(exp_name=exp_name, 
                pane=self.defaults.c_client_pane,
                idx=0, vmid=0, stack=self.cstack,
                ip=self.defaults.server_ip, port=1234, ncores=12,
                msize=msize, mpending=64, nconns=100,
                open_delay=10, max_msgs_conn=0, max_pend_conns=1,
                cset="client",
                bench_dir=self.defaults.default_obenchmark_dir_bare,
                tas_dir=self.defaults.default_otas_dir_bare,
                cores=vm0_cset.cores)
        self.client_configs.append(client0_config)