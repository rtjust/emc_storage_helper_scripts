import sys
import re
from storops import UnitySystem
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


array_user = 'user'
array_pass = 'pass'

#input_file_name = sys.argv[1]
input_file_name = 'unity_list.txt'
with open(input_file_name, 'r') as input_file:
    for ip in input_file.readlines():
        with open(input_file_name[:-4] + '_out' + '.txt', 'a') as file:
            print(ip)
            file.write(ip+'\n')
            array_ip = ip[:-1]
            try:
                unity = UnitySystem(array_ip, array_user, array_pass)
                print('Array: {}'.format(unity.name))
                file.write('Array: {}\n'.format(unity.name))
                filesystems = unity.get_filesystem()
                for fs in filesystems:
                    print(fs)
            except(Exception):
                print(Exception.message)
                continue
