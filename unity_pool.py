import sys
import re
from storops import UnitySystem
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


array_user = 'user'
array_pass = 'pass'

input_file_name = sys.argv[1]
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
                pools = unity.get_pool()
                for pool in pools:
                    print('\tPool: {}'.format(pool.name))
                    file.write('\tPool: {}\n'.format(pool.name))
                    allocated = pool.size_used / pool.size_total
                    subscribed = pool.size_subscribed / pool.size_total
                    print('\tAllocated: {:.2f}'.format(allocated * 100))
                    file.write('\tAllocated: {:.2f}\n'.format(allocated * 100))
                    print('\tSubscribed: {:.2f}'.format(subscribed * 100))
                    file.write('\tSubscribed: {:.2f}\n'.format(subscribed * 100))
                    if subscribed * 100 > 100:
                        print('\t*** Oversubscribed! ***')
                        file.write('\t*** Oversubscribed! ***\n')
                    print()
                    file.write('\n')
            except(Exception):
                continue
