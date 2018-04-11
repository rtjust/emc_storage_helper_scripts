import sys

input_file_name = sys.argv[1]
with open(input_file_name, 'r') as input_file:
    wwn_list = []
    for wwn in input_file:
        colonized_wwn = ''
        trimmed_wwn = ''
        temp_wwn = ''
        if wwn[:4] == 'naa.':
            trimmed_wwn = wwn[4:]
        else:
            trimmed_wwn = wwn
        for i in range(0, len(trimmed_wwn), 2):
            temp_wwn = temp_wwn + trimmed_wwn[i - 2:i] + ':'
        colonized_wwn = temp_wwn[1:-1].upper()
        print(colonized_wwn)
        wwn_list.append(colonized_wwn)
        with open(input_file_name[:-4] + '_out' + '.txt', 'w') as output_file:
            for wwn in wwn_list:
                output_file.write(wwn + '\n')
