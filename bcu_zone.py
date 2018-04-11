import sys
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


account_num = ''
array_num = '\'
array_type = 'UNITY' # 'VNX' or 'UNITY' or 'Unity' depending on the what the port aliases are named
fabric_a_name = ''
fabric_b_name = ''
a_on_top = False
spa_fe_ports = ['SPA0','SPA1', 'SPA2', 'SPA3', 'SPA4', 'SPA5']
spb_fe_ports = ['SPB0','SPB1', 'SPB2', 'SPB3', 'SPB4', 'SPB5']

input_file_name = sys.argv[1]
with open(input_file_name, 'r') as input_file:
    server_re = re.compile(r'(###)( )([0-9]{6})')
    wwn_re = re.compile(r'(fc    )(\b\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\b)')
    input_file = input_file.read()
    server_list = server_re.findall(input_file)
    wwn_list = wwn_re.findall(input_file)
    zone_list = ''
    with open(input_file_name[:-4] + '_A_Side' + '.txt', 'w') as output_file:
        counter = 0
        one_or_three_or_five = 1
        for server in server_list:
            if a_on_top:
                output_file.write('\nalicreate HBA0_{0}, {1}'.format(server[2], wwn_list[counter+1][1]))
            else:
                output_file.write('\nalicreate HBA0_{0}, {1}'.format(server[2], wwn_list[counter+3][1]))

            if one_or_three_or_five == 1:
                output_file.write('\nzonecreate HBA0_{0}_{1}_{3}_{2}, "HBA0_{1}; {3}_{0}_{2}_{4}; {3}_{0}_{2}_{5}"'.format(account_num, server[2], array_num, array_type, spa_fe_ports[1], spb_fe_ports[0]))
                zone_list += 'HBA0_{0}_{1}_{2}_{3};'.format(account_num, server[2], array_type, array_num)
                one_or_three_or_five = 3
            elif one_or_three_or_five == 3:
                output_file.write('\nzonecreate HBA0_{0}_{1}_{3}_{2}, "HBA0_{1}; {3}_{0}_{2}_{4}; {3}_{0}_{2}_{5}"'.format(account_num, server[2], array_num, array_type, spa_fe_ports[3], spb_fe_ports[2]))
                zone_list += 'HBA0_{0}_{1}_{2}_{3};'.format(account_num, server[2], array_type, array_num)
                one_or_three_or_five = 5
            elif one_or_three_or_five == 5:
                output_file.write('\nzonecreate HBA0_{0}_{1}_{3}_{2}, "HBA0_{1}; {3}_{0}_{2}_{4}; {3}_{0}_{2}_{5}"'.format(account_num, server[2], array_num, array_type, spa_fe_ports[5], spb_fe_ports[4]))
                zone_list += 'HBA0_{0}_{1}_{2}_{3};'.format(account_num, server[2], array_type, array_num)
                one_or_three_or_five = 1
            counter += 4
        output_file.write('\ncfgAdd {0}, "{1}"'.format(fabric_a_name, zone_list[:-1]))
    zone_list = ''
    with open(input_file_name[:-4] + '_B_Side' + '.txt', 'w') as output_file:
        counter = 0
        one_or_three_or_five = 1
        for server in server_list:
            if a_on_top:
                output_file.write('\nalicreate HBA1_{0}, {1}'.format(server[2],wwn_list[counter+3][1]))
            else:
                output_file.write('\nalicreate HBA1_{0}, {1}'.format(server[2],wwn_list[counter+1][1]))
            if one_or_three_or_five == 1:
                output_file.write('\nzonecreate HBA1_{0}_{1}_{3}_{2}, "HBA1_{1}; {3}_{0}_{2}_{4}; {3}_{0}_{2}_{5}"'.format(account_num, server[2], array_num, array_type, spa_fe_ports[0], spb_fe_ports[1]))
                zone_list += 'HBA1_{0}_{1}_{2}_{3};'.format(account_num, server[2], array_type, array_num)
                one_or_three_or_five = 3
            elif one_or_three_or_five == 3:
                output_file.write('\nzonecreate HBA1_{0}_{1}_{3}_{2}, "HBA1_{1}; {3}_{0}_{2}_{4}; {3}_{0}_{2}_{5}"'.format(account_num, server[2], array_num, array_type, spa_fe_ports[2], spb_fe_ports[3]))
                zone_list += 'HBA1_{0}_{1}_{2}_{3};'.format(account_num, server[2], array_type, array_num)
                one_or_three_or_five = 5
            elif one_or_three_or_five == 5:
                output_file.write('\nzonecreate HBA1_{0}_{1}_{3}_{2}, "HBA1_{1}; {3}_{0}_{2}_{4}; {3}_{0}_{2}_{5}"'.format(account_num, server[2], array_num, array_type, spa_fe_ports[4], spb_fe_ports[5]))
                zone_list += 'HBA1_{0}_{1}_{2}_{3};'.format(account_num, server[2], array_type, array_num)
                one_or_three_or_five = 1
            counter += 4
        output_file.write('\ncfgAdd {0}, "{1}"'.format(fabric_b_name, zone_list[:-1]))
