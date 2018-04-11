from pexpect import pxssh
import csv
ssh1 = pxssh.pxssh()
unifiedlist = []


def get_dc_pass(datacenter):
    password = ''
    if 'DFW' in datacenter:
        password = 'omitted for github'
    elif 'ORD' in datacenter:
        password = 'omitted for github'
    elif 'IAD' in datacenter:
        password = 'omitted for github'
    elif 'LON' in datacenter:
        password = 'omitted for github'
    elif 'HKG' in datacenter:
        password = 'omitted for github'
    elif 'SYD' in datacenter:
        password = 'omitted for github'
    return password


with open('unifiedlistlon3.csv', 'r') as csvfile:
    unifiedreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    unifiedlist = []
    for row in unifiedreader:
        unifiedlist.append(row)
    for array in unifiedlist:
        dcpass = get_dc_pass(array[0])
        try:
            ssh1 = pxssh.pxssh()
            ssh1.login(array[2], 'user', dcpass)
            print("SSH session login successful " + str(array) + " " + dcpass)
            ssh1.sendline('/nas/bin/nas_emailuser -info')
            ssh1.prompt()         # match the prompt
            print(ssh1.before.decode('UTF-8'))     # print everything before the prompt.
            ssh1.logout()
            ssh1.close()
            print('')
            print('')
        except Exception:
            ssh1.close()
            ssh1 = pxssh.pxssh()
            print("SSH session failed on login. " + str(array) + " " + dcpass)
            try:
                ssh1.login(array[2], 'user', 'pass')
                print("SSH session login successful " + str(array) + " " + 'user')
                ssh1.sendline('/nas/bin/nas_emailuser -info')
                ssh1.prompt()         # match the prompt
                print(ssh1.before.decode('UTF-8'))     # print everything before the prompt.
                ssh1.logout()
                print('')
                print('')
                ssh1.close()
            except Exception:
                print("SSH session failed on login. " + str(array) + " " + 'user')
                ssh1.close()
           # print(str(s))
