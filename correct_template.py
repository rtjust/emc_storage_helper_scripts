import csv
import sys
import os
import subprocess

if 'nt' in os.name:
    # Windows Naviseccli paths
    naviBase = r'"C:\Program Files (x86)\EMC\Navisphere CLI\NaviSECCli.exe" -h {} -t {} {}'
    naviBaseSec = r'"C:\Program Files (x86)\EMC\Navisphere CLI\NaviSECCli.exe" -addusersecurity -user {} -password "{}" -scope 2'
else:
    # Linux Naviseccli paths
    naviBase = '/opt/Navisphere/bin/naviseccli -h {} -t {} {}'
    naviBaseSec = '/opt/Navisphere/bin/naviseccli -addusersecurity -user {} -scope 2'


def naviseccli(ip, command, timeout=60):
    """
    Runs the naviseccli command against the given IP.
    return: tuple (stdout, stderr)
    """
    try:
        process = subprocess.Popen(
            naviBase.format(ip, timeout, command),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
        out, err = process.communicate()
    except Exception as e:
        raise Exception(e)
    return (out.decode(encoding='UTF-8'), err.decode(encoding='UTF-8'))

input_file_name = sys.argv[1]
print('filename: {}'.format(input_file_name))
with open(input_file_name, 'r') as input_file:
    csv_reader = csv.reader(input_file, delimiter=',')
    for row in csv_reader:
        array_name = row[0]
        spa = row[1]
        spb = row[2]
        # result = naviseccli(spa, 'connectemcconfig -m -esrs_priority 1 -email_priority 2'.format())
        # print(result[0], result[1])
        # result = naviseccli(spb, 'connectemcconfig -m -esrs_priority 1 -email_priority 2'.format())
        # print(result[0], result[1])
        result = naviseccli(spa, 'EventMonitor -template -list')
        print(result[0], result[1])
