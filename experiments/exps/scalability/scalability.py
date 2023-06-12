import experiments as exp

from exps.scalability.configs.bare_tas import Config as TasBareConf
from exps.scalability.configs.bare_vtas import Config as VTasBareConf
from exps.scalability.configs.virt_tas import Config as TasVirtConf
# from exps.scalability.configs.ovs_linux import Config as OVSLinuxConf
# from exps.scalability.configs.ovs_tas import Config as OVSTasConf

experiments = []

# n_conns = [1000, 2000, 3000, 4000, 5000]
# n_runs = 3

n_conns = [2000]
n_runs = 1

for n_r in range(n_runs):
  for n_c in n_conns:
    exp_name = "scalability-run{}-conns{}_".format(n_r, n_c)
    tas_bare_exp = exp.Experiment(TasBareConf(exp_name + "bare-tas", n_c), name=exp_name)
    vtas_bare_exp = exp.Experiment(VTasBareConf(exp_name + "bare-vtas", n_c), name=exp_name)
    tas_virt_exp = exp.Experiment(TasVirtConf(exp_name + "virt-tas", n_c), name=exp_name)
    # ovs_linux_exp = exp.Experiment(OVSLinuxConf(exp_name + "ovs-linux", n_c), name=exp_name)
    # ovs_tas_exp = exp.Experiment(OVSTasConf(exp_name + "ovs-tas", n_c), name=exp_name)

    experiments.append(tas_bare_exp)
    experiments.append(vtas_bare_exp)
    experiments.append(tas_virt_exp)
    # experiments.append(ovs_tas_exp)
    # experiments.append(ovs_linux_exp)