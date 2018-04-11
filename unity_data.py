import sys
import re
from storops import UnitySystem
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

array_ip = 'ip'
array_user = 'user'
array_pass = 'pass'

with open(array_ip + '.json', 'w') as file:
    unity = UnitySystem(array_ip, array_user, array_pass)
    # file.writelines(unity.get_sp().json(indent=4))
    # file.writelines(unity.get_dpe().json(indent=4))
    # file.writelines(unity.get_dae().json(indent=4))
    # file.writelines(unity.get_disk().json(indent=4))
    # file.writelines(unity.get_ssd().json(indent=4))
    # file.writelines(unity.get_battery().json(indent=4))
    # file.writelines(unity.get_power_supply().json(indent=4))
    # file.writelines(unity.get_sas_port().json(indent=4))
    # file.writelines(unity.get_ethernet_port().json(indent=4))
    # file.writelines(unity.get_ip_port().json(indent=4))
    # file.writelines(unity.get_lcc().json(indent=4))
    # file.writelines(unity.get_io_module().json(indent=4))
    # file.writelines(unity.get_sas_port().json(indent=4))
    # file.writelines(unity.get_fan().json(indent=4))
    # file.writelines(unity.get_memory_module().json(indent=4))
    # file.writelines(unity.get_license().json(indent=4))
    # file.writelines(unity.get_capability_profile().json(indent=4))
    # file.writelines(unity.get_ssc().json(indent=4))
    # file.writelines(unity.get_disk_group().json(indent=4))
    # file.writelines(unity.get_pool().json(indent=4))
    # file.writelines(unity.get_lun().json(indent=4))
    # file.writelines(unity.get_host().json(indent=4))
    # file.writelines(unity.get_initiator().json(indent=4))
    # file.writelines(unity.get_file_interface().json(indent=4))
    # file.writelines(unity.get_link_aggregation().json(indent=4))
    # file.writelines(unity.get_filesystem().json(indent=4))
    # file.writelines(unity.get_nas_server().json(indent=4))
    # file.writelines(unity.get_nfs_server().json(indent=4))
    # file.writelines(unity.get_nfs_share().json(indent=4))
    # file.writelines(unity.get_cifs_server().json(indent=4))
    # file.writelines(unity.get_cifs_share().json(indent=4))
    print(unity.get_lun())
