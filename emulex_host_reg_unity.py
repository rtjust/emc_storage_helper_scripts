import sys
import re
from storops import UnitySystem
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

array_ip = 'ip_Address'
array_user = ''
array_pass = ''
account_num = ''
array_num = ''
host_type = 'VMware ESXi'

unity = UnitySystem(array_ip, array_user, array_pass)
input_file_name = sys.argv[1]
with open(input_file_name, 'r') as input_file:
    server_re = re.compile(r'(###)( )([0-9]{6})')
    ip_re = re.compile(r'(\$\$\$)( )(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    wwn_re = re.compile(r'(Port WWN       : )(\b\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\b)')
    input_file = input_file.read()
    server_list = server_re.findall(input_file)
    ip_list = ip_re.findall(input_file)
    wwn_list = wwn_re.findall(input_file)
    counter = 0
    for server, ip in zip(server_list, ip_list):
        server_name = '{}-{}'.format(account_num, server[2])
        host = unity.create_host(server_name, os=host_type)
        host.add_initiator('20{0}:{1}'.format(wwn_list[counter+0][1][2:], wwn_list[counter+0][1]))
        host.add_initiator('20{0}:{1}'.format(wwn_list[counter+2][1][2:], wwn_list[counter+2][1]))
        host.add_ip_port(ip[2])
        print('Added {4}-{2} with 20{0}:{1} {3}'.format(wwn_list[counter+0][1][2:], wwn_list[counter+0][1], server[2], ip[2], array_num))
        print('Added {4}-{2} with 20{0}:{1} {3}'.format(wwn_list[counter+2][1][2:], wwn_list[counter+2][1], server[2], ip[2], array_num))
        counter += 4
