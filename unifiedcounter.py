import requests.packages.urllib3
import csv
import datetime
import time
import sys

requests.packages.urllib3.disable_warnings()

apiURL = "omitted for github"

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

def getenablers(array):
    enablerDict = screquest(array, '/enablers/')
    return enablerDict

def screquest(array, request):
    result = requests.get(apiURL + array + request, verify=False).json()
    return result

def count_unified(arrayListInput):
    unifiedArrayList = []
    for array in arrayListInput:
        if array.get('status') == 'online':
            arrayNum = str(array['deviceNumber'])
            model = array.get('model')
            unified = False
            csIPs = False
            print('Device {} is a {}'.format(arrayNum, model))

            if 'VNX' in model:
                arrayDict = {'deviceNumber': str(array['deviceNumber'])}

                ipList = getipaddresses(arrayNum)
                ipListString = ''
                for ip in ipList:
                    ipListString = ipListString + '\n' + ip['name'] + ': ' + ip['ipAddress']
                    if 'cs' in ip['name'].lower():
                        csIPs = True
                        print('cs ips true')

                if csIPs:
                    unified = True

                if unified == True:
                    print('Is Unified')
                    arrayDict = {'deviceNumber': arrayNum}
                    datacenter = array.get('datacenter')
                    serial = ''
                    arrayName = ''
                    osVersion = ''
                    try:
                        arrayName = screquest(arrayNum, '/')['name']
                        osVersion = screquest(arrayNum, '/')['osVersion']
                        serial = {'serial': str(array['manufacturerSerialNumber'])}
                    except:
                        arrayName = 'None'
                        osVersion = 'None'
                        serial = 'None'
                    arrayDict['datacenter'] = datacenter
                    arrayDict['model'] = model
                    arrayDict['osVersion'] = osVersion
                    arrayDict['arrayName'] = arrayName
                    arrayDict['unified'] = unified
                    arrayDict['serial'] = serial
                    arrayDict['ips'] = ipListString

                    unifiedArrayList.append(arrayDict)
        else:
            arrayDict = {'deviceNumber': 'Not able to poll device via API'}
            unifiedArrayList.append(arrayDict)

    return unifiedArrayList

def getipaddresses(array):
    ipAddressList = screquest(array, '/ipaddresses/')
    return ipAddressList

def write_to_csv(arrayList):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H%M%S')
    filename = 'unifiedCounter {}.csv'.format(timestamp)
    with open(filename, 'w') as csvfile:
        fieldnames = ['deviceNumber', 'arrayName', 'datacenter', 'model', 'osVersion', 'unified', 'serial', 'ips']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in arrayList:
            writer.writerow(row)
        csvfile.close()
    print('CSV file created: {}'.format(filename))


write_to_csv(count_unified(get_all_sc_arrays()))
