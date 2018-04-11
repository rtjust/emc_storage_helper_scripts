import csv
import sys
import os

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

input_file_name = sys.argv[2]
sp_ip = sys.argv[1]
print('ip: {} filename: {}'.format(sp_ip, input_file_name))
with open(input_file_name, 'r') as input_file:
    csv_reader = csv.reader(input_file, delimiter=',')
    for row in csv_reader:
        lun_id = row[0]
        lun_name = row[1]
        lun_capacity = row[2]
        lun_pool = row[3]
        print('running: naviseccli -h {} lun -create -type nonThin -capacity {} -poolId {} -aa 1 -l {} -name {}'.format(sp_ip, lun_capacity, lun_pool, lun_id, lun_name))
        result = naviseccli(sp_ip, 'lun -create -type nonThin -capacity {} -poolId {} -aa 1 -l {} -name {}'.format(lun_capacity, lun_pool, lun_id, lun_name))
        print(result[0], result[1])
