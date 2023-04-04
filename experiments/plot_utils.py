
import re

def init_latencies():
  latencies = {
    "50p": 0,
    "90p": 0,
    "99p": 0,
    "99.9p": 0,
    "99.99p": 0
  }

  return latencies

def divide_latencies(latencies, den):
  latencies["50p"] /= den
  latencies["90p"] /= den
  latencies["99p"] /= den
  latencies["99.9p"] /= den
  latencies["99.99p"] /= den

def add_latencies(latencies, fname_c0):
  f = open(fname_c0)
  lines = f.readlines()

  # Latencies are already accumulated over all time
  # period in the logs
  line = lines[len(lines) - 1]
  latencies["50p"] += int(get_50p_lat(line))
  latencies["90p"] += int(get_90p_lat(line))
  latencies["99p"] += int(get_99p_lat(line))
  latencies["99.9p"] += int(get_99_9p_lat(line))
  latencies["99.99p"] += int(get_99_99p_lat(line))

  return latencies

def get_expname_msize(fname):
  regex = "(?<=-msize)[0-9]*"
  msize = re.search(regex, fname).group(0)
  return msize

def get_expname_run(fname):
  run_id_regex = "(?<=-run)[0-9]*"
  run_id = re.search(run_id_regex, fname).group(0)
  return run_id

def get_expname_conns(fname):
  regex = "(?<=-conns)[0-9]*"
  nconns = re.search(regex, fname).group(0)
  return nconns

def get_stack(line):
  stack_regex = "(?<=_)([a-z]+-[a-z]+)(?=_)"
  stack = re.search(stack_regex, line).group(0)
  return stack

def get_client_id(line):
  cid_regex = "(?<=_client)[0-9]*"
  cid = re.search(cid_regex, line).group(0)
  return cid

def get_node_id(line):
  nid_regex = "(?<=_node)[0-9]*"
  nid = re.search(nid_regex, line).group(0)
  return nid

def get_nconns(line):
  nconns_regex = "(?<=_nconns)[0-9]*"
  num = re.search(nconns_regex, line).group(0)
  return num

def get_msize(line):
  msize_regex = "(?<=_msize)[0-9]*"
  msize = re.search(msize_regex, line).group(0)
  return msize

def get_n_messages(line):
  nmessages_regex = "(?<=(n_messages=))(.*?)(?=\ )"
  n_messages = re.search(nmessages_regex, line).group(0)
  return n_messages

def get_cycles_total(line, vmid):
  regex = "(?<=(TVM{}=))(.*?)(?=[\ \n])".format(vmid)
  cycles = re.search(regex, line).group(0)
  return cycles

def get_cycles_rate(line, vmid):
  regex = "(?<=(RVM{}=))(.*?)(?=[\ \n])".format(vmid)
  cycles = re.search(regex, line).group(0)
  return cycles

def get_budget(line, vmid):
  regex = "(?<=(BUVM{}=))(.*?)(?=[\ \n])".format(vmid)
  cycles = re.search(regex, line).group(0)
  return cycles

def get_cycles_poll(line, vmid):
  regex = "(?<=(POLLVM{}=))(.*?)(?=[\ \n])".format(vmid)
  cycles = re.search(regex, line).group(0)
  return cycles

def get_cycles_tx(line, vmid):
  regex = "(?<=(TXVM{}=))(.*?)(?=[\ \n])".format(vmid)
  cycles = re.search(regex, line).group(0)
  return cycles

def get_cycles_rx(line, vmid):
  regex = "(?<=(RXVM{}=))(.*?)(?=[\ \n])".format(vmid)
  cycles = re.search(regex, line).group(0)
  return cycles

def get_50p_lat(line):
  regex = "(?<=(50p=))(.*?)(?=\ )"
  lat = re.search(regex, line).group(0)
  return lat

def get_90p_lat(line):
  regex = "(?<=(90p=))(.*?)(?=\ )"
  lat = re.search(regex, line).group(0)
  return lat

def get_95p_lat(line):
  regex = "(?<=(95p=))(.*?)(?=\ )"
  lat = re.search(regex, line).group(0)
  return lat

def get_99p_lat(line):
  regex = "(?<=(99p=))(.*?)(?=\ )"
  lat = re.search(regex, line).group(0)
  return lat

def get_99_9p_lat(line):
  regex = "(?<=(99\.9p=))(.*?)(?=\ )"
  lat = re.search(regex, line).group(0)
  return lat

def get_99_99p_lat(line):
  regex = "(?<=(99\.99p=))(.*?)(?=\ )"
  lat = re.search(regex, line).group(0)
  return lat

def get_tp(line):
  tp_regex = "(?<=(total=))(.*?)(?=\ )"
  tp = re.search(tp_regex, line).group(0)
  return tp

def get_ts(line):
  ts_regex = "(?<=(ts=))(.*?)(?=\ )"
  ts = re.search(ts_regex, line).group(0)
  return ts

def get_elapsed(line):
  ts_regex = "(?<=(elapsed=))(.*?)(?=\ )"
  ts = re.search(ts_regex, line).group(0)
  return ts

def get_first_ts(fname):
  f = open(fname)
  lines = f.readlines()

  l = lines[0]
  first_ts = get_ts(l)
  return first_ts

def get_last_ts(fname):
  f = open(fname)
  lines = f.readlines()

  l = lines[len(lines) - 1]
  last_ts = get_ts(l)
  return last_ts

def get_min_idx(path, c1_first_ts):
  f = open(path)

  for idx, l in enumerate(f):
    ts = get_ts(l)

    if int(ts) > int(c1_first_ts):
      return idx, ts

  return -1, -1
