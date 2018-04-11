import sys
import re
from storops import UnitySystem
import json

array_ip = ''
array_user = 'user'
array_pass = 'pass'

unity = UnitySystem(array_ip, array_user, array_pass)
luns = unity.get_lun()
for lun in luns:
    lun_id = lun.id
    lun_name = lun.name
    lun_wwn = lun.wwn
    lun_size = lun.size_total / 1024 / 1024 / 1024
    print('Lun ID: {}'.format(lun_id))
    print('Lun Name: {}'.format(lun_name))
    print('Lun Size (GB): {}'.format(lun_size))
    print('Lun WWN: {}'.format(lun.wwn))
    lun_pool = lun.pool.id
    print('Lun Pool: {}'.format(lun_pool))
    print()
