import subprocess
naviBase = "/opt/Navisphere/bin/naviseccli -h {} -user {} -password {} -scope {} -t {} {}"

def naviseccli(ip, user, password, scope, command, timeout=10):
    """
    Runs the naviseccli command against the given IP.
    return: tuple (stdout, stderr)
    """
    try:
        process = subprocess.Popen(
            naviBase.format(ip, user, password, scope, timeout, command),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
        out, err = process.communicate()
    except Exception as e:n
        raise Exception(e)
    return (out.decode(encoding='UTF-8'), err.decode(encoding='UTF-8'))
result = naviseccli('IP', 'admin', 'password', '0', 'storagepool -list')
for key in result:
    print(key)
