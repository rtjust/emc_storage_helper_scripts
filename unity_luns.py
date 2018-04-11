import sys
import re
import csv
from storops import UnitySystem
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


array_user = 'user'
array_pass = ''
array_ip = ''

input_file_name = 'luns.txt'
with open(input_file_name, 'r') as input_file:
    csv_reader = csv.reader(input_file, delimiter=',')
    unity = UnitySystem(array_ip, array_user, array_pass)
    pools = unity.get_pool()
    for lun in csv_reader:
        new_lun_name = lun[0]
        lun_size = int(lun[1])
        pool_id = int(lun[2])
        print('{0} {1} {2}'.format(new_lun_name, lun_size, pool_id))
        pools[pool_id-1].create_lun(lun_name=new_lun_name, is_thin=True, size_gb=lun_size, )
