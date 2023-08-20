""" IP tables may drop packets on the bridge so run the following
    on the host machine if that happens
    echo 0 > /proc/sys/net/bridge/bridge-nf-call-iptables """

class Defaults:
    def __init__(self):
        self.client_ip = '192.168.10.13'
        self.server_ip = '192.168.10.14'

        self.pane_prefix = 'e_'
        self.server_pane_prefix = '{}server'.format(self.pane_prefix)
        self.client_pane_prefix = '{}client'.format(self.pane_prefix)

        # Pane names
        self.s_tas_pane = "{}_tas".format(self.server_pane_prefix)
        self.s_vm_pane = "{}_vm".format(self.server_pane_prefix)
        self.s_proxyg_pane = "{}_proxyg".format(self.server_pane_prefix)
        self.s_proxyh_pane = "{}_proxy_h".format(self.server_pane_prefix)
        self.s_server_pane = "{}".format(self.server_pane_prefix)
        self.s_savelogs_pane = "{}_savelogs".format(self.server_pane_prefix)
        self.s_setup_pane = "{}_setup".format(self.server_pane_prefix)
        self.s_cleanup_pane = "{}_cleanup".format(self.server_pane_prefix)

        self.c_tas_pane = "{}_tas".format(self.client_pane_prefix)
        self.c_vm_pane = "{}_vm".format(self.client_pane_prefix)
        self.c_proxyg_pane = "{}_proxyg".format(self.client_pane_prefix)
        self.c_proxyh_pane = "{}_proxyh".format(self.client_pane_prefix)
        self.c_client_pane = "{}".format(self.client_pane_prefix)
        self.c_savelogs_pane = "{}_savelogs".format(self.client_pane_prefix)
        self.c_setup_pane = "{}_setup".format(self.client_pane_prefix)
        self.c_cleanup_pane = "{}_cleanup".format(self.client_pane_prefix)

        # Mellanox interfaces on client and server machine
        self.client_interface = 'enp216s0f0np0'
        self.client_interface_pci = "0000:d8:00.0"
        self.client_mac = "b8:59:9f:c4:af:e6"
        self.server_interface = 'enp216s0f0np0'
        self.server_interface_pci = "0000:d8:00.0"
        self.server_mac = "b8:59:9f:c4:af:66"

        ### INTERNAL VM CONFIGS ###
        # Network interface used to set ip for a VM
        self.vm_interface = "enp0s3"
        # Network interface used to bind TAS in tap VM
        self.tas_interface = "enp0s3"
        # PCI Id of TAS interface inside a VM
        self.pci_id = "0000:00:03.0"
        ############################

        self.remote_connect_cmd = 'ssh swsnetlab04'

        self.home_dir = '/local/mstolet'
        self.home_dir_virt = '/home/tas'

        self.default_vtas_dir_bare = '{}/projects/tas'.format(self.home_dir)
        self.default_vtas_dir_virt = '{}/projects/tas'.format(self.home_dir_virt)
        self.default_otas_dir_bare = '{}/projects/o-tas/tas'.format(self.home_dir)
        self.default_otas_dir_virt = '{}/projects/o-tas/tas'.format(self.home_dir_virt)

        self.default_vbenchmark_dir_bare = '{}/projects/benchmarks'.format(self.home_dir)
        self.default_vbenchmark_dir_virt = '{}/projects/benchmarks'.format(self.home_dir_virt)
        self.default_obenchmark_dir_bare = '{}/projects/o-benchmarks/benchmarks'.format(self.home_dir)
        self.default_obenchmark_dir_virt = '{}/projects/o-benchmarks/benchmarks'.format(self.home_dir_virt)

        self.ovs_ctl_path = "/usr/local/share/openvswitch/scripts/ovs-ctl"
        self.original_ovs_path = "/local/mstolet/projects/o-ovs/ovs"
        self.modified_ovs_path = "/local/mstolet/projects/ovs"

class MachineConfig:
    def __init__(self, ip, interface, stack, is_remote, is_server):
        self.is_server = is_server
        self.is_remote = is_remote
        self.interface = interface
        self.ip = ip
        self.stack = stack

class TasConfig:
    def __init__(self, pane, machine_config, project_dir, ip, n_cores, 
            dpdk_extra="d8:00.0", cc="timely", 
            cc_timely_min_rtt="15",
            cc_timely_tlow="30", cc_timely_thigh="2000",
            cc_timely_beta="0.3", cc_timely_alpha="0.02",
            cc_timely_minrate="10000", cc_timely_step="40000"):
        self.name = "server" if machine_config. is_server else "client"
        
        self.project_dir = project_dir
        
        self.out_dir = self.project_dir + '/out'
        self.out_file = ''
        if machine_config.is_server:
            self.out_file = 'tas_s'
        else:
            self.out_file = 'tas_c'
        self.out = self.out_dir + '/' + self.out_file
        
        self.comp_dir = self.project_dir
        self.comp_cmd = 'make -j6'
        self.clean_cmd = 'make clean'
        self.lib_so = self.comp_dir + 'lib/libtas_interpose.so'
        self.exec_file = self.comp_dir + '/tas/tas'
        self.args = '--ip-addr={}/24 --fp-cores-max={}'.format(ip, n_cores) + \
            ' --fp-no-autoscale --fp-no-ints' + \
            ' --cc={}'.format(cc) + \
            ' --dpdk-extra="-a{}"'.format(dpdk_extra)   
        
        if cc == "timely":
            self.args = self.args + " --cc-timely-minrtt={}".format(cc_timely_min_rtt)
            self.args = self.args + " --cc-timely-tlow={}".format(cc_timely_tlow)
            self.args = self.args + " --cc-timely-thigh={}".format(cc_timely_thigh)
            self.args = self.args + " --cc-timely-beta={}".format(cc_timely_beta)
            self.args = self.args + " --cc-timely-alpha={}".format(cc_timely_alpha)
            self.args = self.args + " --cc-timely-minrate={}".format(cc_timely_minrate)
            self.args = self.args + " --cc-timely-step={}".format(cc_timely_step)

        self.pane = pane
        self.ip = ip
        self.n_cores = n_cores

class VMConfig:
    def __init__(self, pane, machine_config, tas_dir, tas_dir_virt, idx,
                 n_cores, memory, n_queues=None):
        self.name = "server" if machine_config.is_server else "client"
        
        self.manager_dir = tas_dir + '/images'
        self.manager_dir_virt = tas_dir_virt + '/images'
        
        self.pane = pane
        self.id = idx

        self.n_cores = n_cores
        self.memory = memory
        self.n_queues = n_queues
        if machine_config.is_server:
            self.vm_ip = '192.168.10.{}'.format(20 + idx)
            self.tas_tap_ip = '10.0.1.{}'.format(1 + idx)
        else:
            self.vm_ip = '192.168.10.{}'.format(40 + idx)
            self.tas_tap_ip = '10.0.1.{}'.format(20 + idx)

class ProxyConfig:
    def __init__(self, machine_config, comp_dir):
        self.name = "server" if machine_config.is_server else "client"
        
        self.out_dir = comp_dir + "/out"
        
        self.ivshm_socket_path = '/run/tasproxy'
        
        self.comp_dir = comp_dir
        self.comp_cmd = 'make -j6'
        self.clean_cmd = 'make clean'

class HostProxyConfig(ProxyConfig):
    def __init__(self, pane, machine_config, comp_dir):
        ProxyConfig.__init__(self, machine_config, comp_dir)
        self.exec_file = self.comp_dir + '/proxy/host/host'
        
        self.out_file = 'proxy_h'
        self.out = self.out_dir + '/' + self.out_file
        
        self.pane = pane

class GuestProxyConfig(ProxyConfig):
    def __init__(self, pane, machine_config, comp_dir):
        ProxyConfig.__init__(self, machine_config, comp_dir)
        self.exec_file = self.comp_dir + '/proxy/guest/guest'
       
        self.out_file = 'proxy_g'
        self.out = self.out_dir + '/' + self.out_file
       
        self.pane = pane

class ClientConfig:
    def __init__(self, pane, idx, vmid,
            ip, port, ncores, msize, mpending,
            nconns, open_delay, max_msgs_conn, max_pend_conns,
            bench_dir, tas_dir, stack, exp_name, 
            bursty=0, burst_length_mean=0, burst_interval_mean=0, groupid=0):
        self.name = "client"
        self.exp_name = exp_name
        self.exp_name = ""
        self.tas_dir = tas_dir
       
        self.comp_dir = bench_dir + "/micro_rpc"
        self.comp_cmd = 'make -j6'
        self.clean_cmd = 'make clean'
       
        self.bench_dir = bench_dir
        self.lib_so = tas_dir + '/lib/libtas_interpose.so'
        self.exec_file = self.comp_dir + '/testclient_linux'
       
        self.out_dir = tas_dir + "/out"
        self.out_file = "{}_client{}_node{}_nconns{}_ncores{}_msize{}".format(
                exp_name, idx, vmid, nconns, ncores, msize)
        self.latency_file = self.out_file + "_latency_hist"
        self.temp_file = "temp"
        self.out = self.out_dir + '/' + self.out_file
        self.latency_out = self.out_dir + "/" + self.latency_file
        self.latency_temp = self.out_dir + "/" + self.temp_file
       
        self.args = '{} {} {} foo {} {} {} {} {} {} {} {} {} {} {}'.format(ip, port, ncores, \
            msize, mpending, nconns, open_delay, \
            max_msgs_conn, max_pend_conns, \
            bursty, burst_length_mean, burst_interval_mean, \
            self.out_dir + "/", self.latency_file)

        self.groupid = groupid
        self.pane = pane
        self.id = idx
        self.stack = stack

class ServerConfig:
    def __init__(self, pane, idx, vmid,
            port, ncores, max_flows, max_bytes,
            bench_dir, tas_dir, groupid=0):
        self.name = "server"
        self.tas_dir = tas_dir
        
        self.bench_dir = bench_dir
        self.comp_dir = bench_dir + "/micro_rpc"
        self.comp_cmd = 'make -j6'
        self.clean_cmd = 'make clean'
        self.lib_so = tas_dir + '/lib/libtas_interpose.so'
        self.exec_file = self.comp_dir + '/echoserver_linux'
        self.args = '{} {} foo {} {}'.format(port, ncores, \
                max_flows, max_bytes)
        
        self.out_dir = tas_dir + "/out"
        self.out_file = 'rpc_s'
        self.out = self.out_dir + '/' + self.out_file
        
        self.groupid = groupid
        self.pane = pane
        self.id = idx
        self.vmid = vmid
