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


input_file_name = sys.argv[2]
sp_ip = sys.argv[1]
print('ip: {} filename: {}'.format(sp_ip, input_file_name))
with open(input_file_name, 'r') as input_file:
    csv_reader = csv.reader(input_file, delimiter=',')
    for row in csv_reader:
        host_name = row[0]
        host_ip = row[1]
        hba_uid = row[2]
        spa_port = row[3]
        spb_port = row[4]
        print('running: naviseccli -h {} storagegroup -setpath -o -gname ~management -hbauid {} -sp {} -spport {} -ip {} -host {} -failovermode 4 -arraycommpath 1'.format(
            sp_ip, hba_uid, spa_port[:1], spa_port[1:], host_ip, host_name))
        result_a = naviseccli(sp_ip, 'storagegroup -setpath -o -gname ~management -hbauid {} -sp {} -spport {} -ip {} -host {} -failovermode 4 -arraycommpath 1'.format(
            hba_uid, spa_port[:1], spa_port[1:], host_ip, host_name))
        print(result_a[0], result_a[1])
        print('running: naviseccli -h {} storagegroup -setpath -o -gname ~management -hbauid {} -sp {} -spport {} -ip {} -host {} -failovermode 4 -arraycommpath 1'.format(
            sp_ip, hba_uid, spb_port[:1], spb_port[1:], host_ip, host_name))
        result_b = naviseccli(sp_ip, 'storagegroup -setpath -o -gname ~management -hbauid {} -sp {} -spport {} -ip {} -host {} -failovermode 4 -arraycommpath 1'.format(
            hba_uid, spb_port[:1], spb_port[1:], host_ip, host_name))
        print(result_b[0], result_b[1])
