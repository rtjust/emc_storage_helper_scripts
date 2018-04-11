import sys
import re

account_num = ''
array_num = ''
fabric_a_name = ''
fabric_b_name = ''

input_file_name = sys.argv[1]
with open(input_file_name, 'r') as input_file:
    server_re = re.compile(r'(###)( )([0-9]{6})')
    wwn_re = re.compile(
        r'(Port WWN       : )(\b\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\b)'
    )
    input_file = input_file.read()
    server_list = server_re.findall(input_file)
    wwn_list = wwn_re.findall(input_file)
    zone_list = ''
    with open(input_file_name[:-4] + '_A_Side' + '.txt', 'w') as output_file:
        counter = 0
        one_or_three = 1
        for server in server_list:
            output_file.write('\nalicreate HBA0_{0}, {1}'.format(
                server[2], wwn_list[counter + 2][1]))
            if one_or_three == 1:
                output_file.write(
                    '\nzonecreate HBA0_{0}_{1}, "HBA0_{1}; UNITY_{0}_{2}_SPA1; UNITY_{0}_{2}_SPB0"'.
                    format(account_num, server[2], array_num))
                zone_list += 'HBA0_{0}_{1};'.format(account_num, server[2])
                one_or_three = 3
            else:
                output_file.write(
                    '\nzonecreate HBA0_{0}_{1}, "HBA0_{1}; UNITY_{0}_{2}_SPA3; UNITY_{0}_{2}_SPB2"'.
                    format(account_num, server[2], array_num))
                zone_list += 'HBA0_{0}_{1};'.format(account_num, server[2])
                one_or_three = 1
            counter += 4
        output_file.write('\ncfgAdd {0}, "{1}"'.format(fabric_a_name,
                                                       zone_list[:-1]))
    zone_list = ''
    with open(input_file_name[:-4] + '_B_Side' + '.txt', 'w') as output_file:
        counter = 0
        one_or_three = 1
        for server in server_list:
            output_file.write('\nalicreate HBA1_{0}, {1}'.format(
                server[2], wwn_list[counter + 0][1]))
            if one_or_three == 1:
                output_file.write(
                    '\nzonecreate HBA1_{0}_{1}, "HBA1_{1}; UNITY_{0}_{2}_SPA0; UNITY_{0}_{2}_SPB1"'.
                    format(account_num, server[2], array_num))
                zone_list += 'HBA1_{0}_{1};'.format(account_num, server[2])
                one_or_three = 3
            else:
                output_file.write(
                    '\nzonecreate HBA1_{0}_{1}, "HBA1_{1}; UNITY_{0}_{2}_SPA2; UNITY_{0}_{2}_SPB3"'.
                    format(account_num, server[2], array_num))
                zone_list += 'HBA1_{0}_{1};'.format(account_num, server[2])
                one_or_three = 1
            counter += 4
        output_file.write('\ncfgAdd {0}, "{1}"'.format(fabric_b_name,
                                                       zone_list[:-1]))
