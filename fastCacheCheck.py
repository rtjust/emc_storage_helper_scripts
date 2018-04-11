import requests
import requests.packages.urllib3
import csv
requests.packages.urllib3.disable_warnings()

url = "omitted for github"
print('Please wait while fetching array list from StorageCenter API...')
apiArraysDict = requests.get(url + '?page=0', verify=False).json()['result']
print('Page 1 of 4 completed')
apiArraysDict.extend(requests.get(url + '?page=1', verify=False).json()['result'])
print('Page 2 of 4 completed')
apiArraysDict.extend(requests.get(url + '?page=2', verify=False).json()['result'])
print('Page 3 of 4 completed')
apiArraysDict.extend(requests.get(url + '?page=4', verify=False).json()['result'])
print('Page 4 of 4 completed')
print('Now processing {} arrays'.format(len(apiArraysDict)))
fcArrayList = []

for array in apiArraysDict:
    print(array['deviceNumber'])
    enablerDict = requests.get(url + str(array['deviceNumber']) + "/enablers/", verify=False)
    for enabler in enablerDict.json():
        if enabler['packageName'] == "-FASTCache":
            print("FastCache enabler is installed")
            arrayDict = {'deviceNumber': str(array['deviceNumber'])}
            try:
                fastCacheState = requests.get(url + str(array['deviceNumber']) + "/fastCache/", verify=False)
                if fastCacheState.json().get('state') == "Enabled":
                    print("FastCache is enabled on array")
                    poolsDict = requests.get(url + str(array['deviceNumber']) + "/pools/", verify=False)
                    enabledPools = ""
                    disabledPools = ""
                    unknownStatePools = ""
                    disabledPoolsCount = 0
                    for pool in poolsDict.json():
                        poolInfo = requests.get(url + str(array['deviceNumber']) + "/pools/" + str(pool['poolID']), verify=False)
                        if poolInfo.json().get('fastcacheEnabled') == "Enabled":
                            print(poolInfo.json().get('poolName') + " has FastCache enabled")
                            enabledPools += poolInfo.json().get('poolName') + '\n'
                        elif poolInfo.json().get('fastcacheEnabled') == "Disabled":
                            print(poolInfo.json().get('poolName') + " has FastCache disabled")
                            disabledPools += poolInfo.json().get('poolName') + '\n'
                            disabledPoolsCount += 1
                        else:
                            print(poolInfo.json().get('poolName') + ", unable to determine FastCache state?")
                            unknownStatePools += poolInfo.json().get('poolName') + '\n'
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

with open('fastCacheArrayList.csv', 'w') as csvfile:
    fieldnames = ['deviceNumber', 'enabledPools', 'disabledPools', 'unknownStatePools']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in fcArrayList:
        writer.writerow(row)
    csvfile.close()
