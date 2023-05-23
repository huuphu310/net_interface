from f_netplan import netplan
import yaml
import glob
from datetime import datetime
import shutil

path = '/etc/netplan'

files = glob.glob(path + "/*.yaml")
p = netplan.Parser()

def create_fixed_file(interface, data):
    data['version'] = 2
    data = {'network': data}
    with open(path + '/' + interface + '.yaml', mode='w') as f:
        print(yaml.dump(data), file=f, end='')

for file in files:
    try:
        shutil.copy(file, file + '.bak-' +str(datetime.now().strftime('%Y%m%d.%H%m%S')))
        fix = {}
        data = p.parse(include=file)
        for interface in data.data.keys():
            try:
                for iface, cfg in data.get_all_interfaces([interface]).data.items():
                    if cfg.section not in fix:
                        fix[cfg.section] = {}
                    cfg.set('link-local',[])
                    fix[cfg.section][iface] = cfg.data
            except Exception as e:
                print(e)
                pass
        fix['version'] = 2
        fix = {'network': fix}
        with open(file, mode='w') as f:
            print(yaml.dump(fix), file=f, end='')
    except:
        pass

# for file in files:
#     try:
#         fix = {}
#         data = p.parse(include=file)
#         for interface in data.data.keys():
#             try:
#                 for iface, cfg in data.get_all_interfaces([interface]).data.items():
#                     cfg.set('link-local', [ 'ipv4' ])
#                 fix[cfg.section] = {iface: cfg.data}
#                 create_fixed_file(interface, fix)
#             except:
#                 pass
#         os.remove(file)
#     except:
#         pass
