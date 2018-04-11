import requests.packages.urllib3
import csv
import datetime
import time
import sys

requests.packages.urllib3.disable_warnings()

apiURL = "omitted for github"


def screquest(array, request):
    if isinstance(array, str):
        result = requests.get(apiURL + array + request, verify=False).json()
    else:
        result = requests.get(apiURL + str(array['deviceNumber']) + request, verify=False).json()
    return result


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


def count_viper_drives(arrayListInput):
    viperArrayList = []
    for array in arrayListInput:
        viperDiskCount = 0
        model = array.get('model')
        print('Device {} is a {}'.format(str(array['deviceNumber']), model))
        if 'CX' in model or 'VNX' in model:
            disksDict = screquest(array, "/disks/")
            for disk in disksDict:
                if "005049675" in disk.get('clariionTLAPartNumber') or "005049677" in disk.get('clariionTLAPartNumber'):
                    if 'C840' not in disk.get('productRevision'):
                        viperDiskCount += 1
            if viperDiskCount > 0:
                print('Found {} affected Viper drives'.format(viperDiskCount))
                arrayDict = {'deviceNumber': str(array['deviceNumber'])}
                status = array.get('status')
                datacenter = array.get('datacenter')
                try:
                    arrayName = screquest(array, '/')['name']
                    osVersion = screquest(array, '/')['osVersion']
                except:
                    arrayName = 'None'
                    osVersion = 'None'
                arrayDict['status'] = status
                arrayDict['datacenter'] = datacenter
                arrayDict['model'] = model
                arrayDict['osVersion'] = osVersion
                arrayDict['arrayName'] = arrayName
                arrayDict['viperDiskCount'] = viperDiskCount
                viperArrayList.append(arrayDict)
            else:
                print('No affected Viper drives found.')
    return viperArrayList


def write_to_csv(arrayList):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H%M%S')
    filename = 'viperCounter {}.csv'.format(timestamp)
    with open(filename, 'w') as csvfile:
        fieldnames = ['deviceNumber', 'arrayName', 'datacenter', 'status', 'model', 'osVersion', 'viperDiskCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in arrayList:
            writer.writerow(row)
        csvfile.close()
    print('CSV file created: {}'.format(filename))


if len(sys.argv) < 2:
    print(
        'This will gather all arrays from StorageCenter and process them to count Viper drives with firmware != C840.')
    try:
        write_to_csv(count_viper_drives(get_all_sc_arrays()))
    except Exception as e:
        print(e)
else:
    print(
        'This will process the arrays provided as arguments and process '
        'them to count Viper drives with firmware != C840.')
    try:
        inputList = sys.argv[1:]
        print('Input arrays: ' + str(inputList))
        arrayList = []
        for array in inputList:
            arrayList.append(screquest(array, '/'))
        count_viper_drives(arrayList)
    except Exception as e:
        print(e)
