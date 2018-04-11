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

input_file_name = sys.argv[3]
source_sp_ip = sys.argv[1]
target_sp_ip = sys.argv[2]
print('ips: {} {} filename: {}'.format(source_sp_ip, target_sp_ip, input_file_name))
with open(input_file_name, 'r') as input_file:
    csv_reader = csv.reader(input_file, delimiter=',')
    for row in csv_reader:

        source_lun_id = row[0]
        mirror_name = row[1]
        target_lun_id = row[2]
        # create mirror
        print('running: naviseccli -h {} mirror -async -create -name {} -lun {} -requiredimages 1 -o'.format(source_sp_ip, mirror_name, source_lun_id))
        result_createmirror = naviseccli(source_sp_ip, 'mirror -async -create -name {} -lun {} -requiredimages 1 -o'.format(mirror_name, source_lun_id))
        print(result_createmirror[0], result_createmirror[1])
        # add image to mirror
        print('running: naviseccli -h {} mirror -async -addimage -name {} -arrayhost {} -lun {} -syncrate low -enddelay 15'.format(source_sp_ip, mirror_name, target_sp_ip, target_lun_id))
        result_addimage = naviseccli(source_sp_ip, 'mirror -async -addimage -name {} -arrayhost {} -lun {} -syncrate low -enddelay 15'.format(mirror_name, target_sp_ip, target_lun_id))
        print(result_addimage[0], result_addimage[1])
