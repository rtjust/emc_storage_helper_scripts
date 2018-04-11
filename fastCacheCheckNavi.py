import requests.packages.urllib3
import csv
import subprocess
import sys
import datetime
import time

requests.packages.urllib3.disable_warnings()

apiURL = "omitted for github"
naviBase = "/opt/Navisphere/bin/naviseccli -h {} -user {} -password {} -scope {} -t {} {}"

# 'navi' uses navicli to check fastcache pool state, 'api' uses api, unsupported by api at this time
SCRIPT_MODE = 'navi'


def get_all_sc_arrays():
    print('Please wait while fetching array list from StorageCenter API...')
    apiArraysDict = requests.get(apiURL + '?page=0', verify=False).json()['result']
    print('Page 1 of 4 completed')
    apiArraysDict.extend(requests.get(apiURL + '?page=1', verify=False).json()['result'])
    print('Page 2 of 4 completed')
    apiArraysDict.extend(requests.get(apiURL + '?page=2', verify=False).json()['result'])
    print('Page 3 of 4 completed')
    apiArraysDict.extend(requests.get(apiURL + '?page=4', verify=False).json()['result'])
    print('Page 4 of 4 completed')
    print('Found {} arrays'.format(len(apiArraysDict)))

    return apiArraysDict


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
    except Exception as e:
        raise Exception(e)
    return out.decode(encoding='UTF-8'), err.decode(encoding='UTF-8')


def getpools(array):
    poolsDict = screquest(array, '/pools/')
    return poolsDict


def getenablers(array):
    enablerDict = screquest(array, '/enablers/')
    return enablerDict


def getipaddresses(array):
    ipAddressList = screquest(array, '/ipaddresses/')
    return ipAddressList


def screquest(array, request):
    if isinstance(array, str):
        result = requests.get(apiURL + array + request, verify=False).json()
    else:
        result = requests.get(apiURL + str(array['deviceNumber']) + request, verify=False).json()
    return result


def getfastcachestate(array):
    fastCacheState = screquest(array, '/fastCache/')
    return fastCacheState


def get_pools_with_fc(arrayDictInput):
    fcArrayList = []
    for array in arrayDictInput:
        print(array['deviceNumber'])
        enablerDict = getenablers(array)
        arrayDict = {'deviceNumber': str(array['deviceNumber'])}
        for enabler in enablerDict:
            if enabler['packageName'] == "-FASTCache":
                print("FastCache enabler is installed")
                try:
                    fastCacheState = getfastcachestate(array)
                    if fastCacheState.get('state') == "Enabled":
                        print("FastCache is enabled on array")
                        poolsDict = getpools(array)
                        enabledPools = ""
                        disabledPools = ""
                        unknownStatePools = ""
                        disabledPoolsCount = 0
                        spIPs = []
                        if SCRIPT_MODE == 'navi':
                            spIPs = getipaddresses(array)
                            print(spIPs[0]['ipAddress'], spIPs[1]['ipAddress'])
                        for pool in poolsDict:
                            poolInfo = requests.get(
                                apiURL + str(array['deviceNumber']) + "/pools/" + str(pool['poolID']),verify=False)
                            if SCRIPT_MODE == 'navi':
                                try:
                                    naviResult1 = naviseccli(spIPs[0]['ipAddress'], 'user', 'pass', '0',
                                                            'storagepool -list -id {} -fastcache'.format(pool['poolID']))
                                    print(naviResult1)
                                except Exception as e:
                                    print(e, 'naviResult1 fail')
                                    naviResult1 = 'fail'

                                try:
                                    naviResult2 = naviseccli(spIPs[1]['ipAddress'], 'user', 'pass', '0',
                                                            'storagepool -list -id {} -fastcache'.format(pool['poolID']))
                                    print(naviResult2)
                                except Exception as e:
                                    print(e, 'naviResult2 fail')
                                    naviResult2 = 'fail'

                                if 'enabled' in naviResult1[0].lower() or 'enabled' in naviResult2[0].lower():
                                    print(poolInfo.json().get('poolName') +
                                          " has FastCache enabled")
                                    enabledPools += poolInfo.json().get(
                                        'poolName') + '\n'
                                elif 'disabled' in naviResult1[0].lower() or 'disabled' in naviResult2[0].lower():
                                    print(poolInfo.json().get('poolName') +
                                          " has FastCache disabled")
                                    disabledPools += poolInfo.json().get(
                                        'poolName') + '\n'
                                    disabledPoolsCount += 1
                                else:
                                    print(poolInfo.json().get('poolName') +
                                          ", unable to determine FastCache state?")
                                    unknownStatePools += poolInfo.json().get(
                                        'poolName') + '\n'
                                    disabledPoolsCount += 1
                            elif SCRIPT_MODE == 'api':
                                if poolInfo.json().get(
                                        'fastcacheEnabled') == "Enabled":
                                    print(poolInfo.json().get('poolName') +
                                          " has FastCache enabled")
                                    enabledPools += poolInfo.json().get(
                                        'poolName') + '\n'
                                elif poolInfo.json().get(
                                        'fastcacheEnabled') == "Disabled":
                                    print(poolInfo.json().get('poolName') +
                                          " has FastCache disabled")
                                    disabledPools += poolInfo.json().get(
                                        'poolName') + '\n'
                                    disabledPoolsCount += 1
                                else:
                                    print(poolInfo.json().get('poolName') +
                                          ", unable to determine FastCache state?")
                                    unknownStatePools += poolInfo.json().get(
                                        'poolName') + '\n'
                                    disabledPoolsCount += 1

                        if disabledPoolsCount >= 1:
                            arrayDict['enabledPools'] = enabledPools
                            arrayDict['disabledPools'] = disabledPools
                            arrayDict['unknownStatePools'] = unknownStatePools
                            fcArrayList.append(arrayDict)
                    else:
                        print("FastCache is disabled on array")
                except Exception as e:
                    print(e)
        print("FastCache enabler is not installed")
    return fcArrayList


def write_to_csv(arrayList):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H%M%S')
    with open('fastCacheArrayList {}.csv'.format(timestamp), 'w') as csvfile:
        fieldnames = ['deviceNumber', 'enabledPools', 'disabledPools',
                      'unknownStatePools']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in arrayList:
            writer.writerow(row)
        csvfile.close()

if len(sys.argv) < 2:
    print('This will gather all arrays from StorageCenter and process them to determine fast cache state on pools.')
    try:
        write_to_csv(get_pools_with_fc(get_all_sc_arrays()))
    except Exception as e:
        print(e)
else:
    print('This will process the arrays provided as arguments and process them to determine fast cache state on pools.')
    try:
        inputList = sys.argv[1:]
        print('Input arrays: ' + str(inputList))
        arrayList = []
        for array in inputList:
            arrayList.append(screquest(array, '/'))
        get_pools_with_fc(arrayList)
    except Exception as e:
        print(e)
