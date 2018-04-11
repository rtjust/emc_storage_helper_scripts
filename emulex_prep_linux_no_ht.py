import sys
import re

input_file_name = sys.argv[1]
with open(input_file_name, 'r') as input_file:
    server_re = re.compile(r'(###)( )([0-9]{6})')
    wwn_re = re.compile(r'(Port WWN       : )(\b\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\b)')
    input_file = input_file.read()
    server_list = server_re.findall(input_file)
    wwn_list = wwn_re.findall(input_file)
    with open(input_file_name[:-4] + '__out' + '.sh', 'w') as output_file:
        counter = 0
        for server in server_list:
            #output_file.write('\nht ' + server[2] + '\n')
            output_file.write('\n')
            output_file.write('\nhbacmd HbaAttributes {}'.format(wwn_list[counter][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd HbaAttributes {}'.format(wwn_list[counter+1][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd HbaAttributes {}'.format(wwn_list[counter+2][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd HbaAttributes {}'.format(wwn_list[counter+3][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd EnableBootCode {} d'.format(wwn_list[counter][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd EnableBootCode {} d'.format(wwn_list[counter+1][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd EnableBootCode {} d'.format(wwn_list[counter+2][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd EnableBootCode {} d'.format(wwn_list[counter+3][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd PortAttributes {}'.format(wwn_list[counter][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd PortAttributes {}'.format(wwn_list[counter+1][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd PortAttributes {}'.format(wwn_list[counter+2][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd PortAttributes {}'.format(wwn_list[counter+3][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd GetXcvrData {}'.format(wwn_list[counter][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd GetXcvrData {}'.format(wwn_list[counter+1][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd GetXcvrData {}'.format(wwn_list[counter+2][1], server[2]))
            output_file.write('\n')
            output_file.write('\nhbacmd GetXcvrData {}\n'.format(wwn_list[counter+3][1], server[2]))
            #output_file.write('\nexit')
            output_file.write('\n')
            counter += 4
