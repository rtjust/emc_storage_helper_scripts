import requests.packages.urllib3
import csv
import datetime
import time
import sys

requests.packages.urllib3.disable_warnings()

apiURL = "omitted for github"


def screquest(array, request):
    result = requests.get(apiURL + array + request, verify=False).json()
    return result

def count_viper_drives(arrayListInput):
    viperArrayList = []
    for array in arrayListInput:
        if array.get('status') == 'online':
            arrayNum = str(array['deviceNumber'])
            viperDiskCount = 0
            model = array.get('model')
            unified = False
            flare = False
            print('Device {} is a {}'.format(arrayNum, model))

            if 'CX' in model or 'VNX' in model:
                ipList = getipaddresses(arrayNum)
                for ip in ipList:
                    print(ip['name'])
                    if 'CS' in ip['name']:
                        unified = True

                disksDict = screquest(arrayNum, "/disks/")
                for disk in disksDict:
                    if '005049675' in disk.get('clariionTLAPartNumber') or '005049677' in disk.get('clariionTLAPartNumber'):
                        print(disk.get('diskID'))
                        if 'C840' not in disk.get('productRevision'):
                            if '0_0_0' == disk.get('diskID') or '0_0_1' == disk.get('diskID') or '0_0_2' == disk.get('diskID') or '0_0_3' == disk.get('diskID'):
                                flare = True
                                print(flare)
                            viperDiskCount += 1

                print('Found {} affected Viper drives'.format(viperDiskCount))
                arrayDict = {'deviceNumber': arrayNum}
                datacenter = array.get('datacenter')
                try:
                    arrayName = screquest(arrayNum, '/')['name']
                    osVersion = screquest(arrayNum, '/')['osVersion']
                except:
                    arrayName = 'None'
                    osVersion = 'None'
                arrayDict['datacenter'] = datacenter
                arrayDict['model'] = model
                arrayDict['osVersion'] = osVersion
                arrayDict['arrayName'] = arrayName
                arrayDict['viperDiskCount'] = viperDiskCount
                arrayDict['unified'] = unified
                arrayDict['flare'] = flare
                viperArrayList.append(arrayDict)
        else:
            arrayDict = {'deviceNumber': 'Not able to poll device via API'}
            viperArrayList.append(arrayDict)

    return viperArrayList

def getipaddresses(array):
    ipAddressList = screquest(array, '/ipaddresses/')
    return ipAddressList

def write_to_csv(arrayList):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H%M%S')
    filename = 'viperCounterPSU {}.csv'.format(timestamp)
    with open(filename, 'w') as csvfile:
        fieldnames = ['deviceNumber', 'arrayName', 'datacenter', 'model', 'osVersion', 'viperDiskCount', 'flare', 'unified']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in arrayList:
            writer.writerow(row)
        csvfile.close()
    print('CSV file created: {}'.format(filename))


inputFile = sys.argv[1]
print(sys.argv[1])
with open(inputFile, 'r') as input_file:
    arrayList = []
    for arrayNum in input_file:
        print(arrayNum.strip())
        arrayList.append(screquest(arrayNum.strip(), '/'))
    write_to_csv(count_viper_drives(arrayList))
