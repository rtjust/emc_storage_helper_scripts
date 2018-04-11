import sys
import re

input_file_name = sys.argv[1]
with open(input_file_name, 'r') as input_file:
    server_re = re.compile(r'(###)( )([0-9]{6})')
    wwn_re = re.compile(r'(Port WWN       : )(\b\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\b)')
    input_file = input_file.read()
    server_list = server_re.findall(input_file)
    wwn_list = wwn_re.findall(input_file)
    with open(input_file_name[:-4] + '_out' + '.txt', 'w') as output_file:
        counter = 0
        for server in server_list:
            output_file.write('\n{}\n'.format(server))
            output_file.write('\nesxcli elxmgmt hbaattributes -w {}'.format(wwn_list[counter][1], server[2]))
            output_file.write('\nesxcli elxmgmt hbaattributes -w {}'.format(wwn_list[counter+1][1], server[2]))
            output_file.write('\nesxcli elxmgmt hbaattributes -w {}'.format(wwn_list[counter+2][1], server[2]))
            output_file.write('\nesxcli elxmgmt hbaattributes -w {}'.format(wwn_list[counter+3][1], server[2]))
            output_file.write('\nesxcli elxmgmt enablebootcode -w {} -s D'.format(wwn_list[counter][1], server[2]))
            output_file.write('\nesxcli elxmgmt enablebootcode -w {} -s D'.format(wwn_list[counter+1][1], server[2]))
            output_file.write('\nesxcli elxmgmt enablebootcode -w {} -s D'.format(wwn_list[counter+2][1], server[2]))
            output_file.write('\nesxcli elxmgmt enablebootcode -w {} -s D'.format(wwn_list[counter+3][1], server[2]))
            output_file.write('\nesxcli elxmgmt portattributes -w {}'.format(wwn_list[counter][1], server[2]))
            output_file.write('\nesxcli elxmgmt portattributes -w {}'.format(wwn_list[counter+1][1], server[2]))
            output_file.write('\nesxcli elxmgmt portattributes -w {}'.format(wwn_list[counter+2][1], server[2]))
            output_file.write('\nesxcli elxmgmt portattributes -w {}'.format(wwn_list[counter+3][1], server[2]))
            output_file.write('\nesxcli elxmgmt getxcvrdata -w {} -t 1'.format(wwn_list[counter][1], server[2]))
            output_file.write('\nesxcli elxmgmt getxcvrdata -w {} -t 1'.format(wwn_list[counter+1][1], server[2]))
            output_file.write('\nesxcli elxmgmt getxcvrdata -w {} -t 1'.format(wwn_list[counter+2][1], server[2]))
            output_file.write('\nesxcli elxmgmt getxcvrdata -w {} -t 1\n'.format(wwn_list[counter+3][1], server[2]))
            counter += 4
