import requests
import requests.packages.urllib3
import csv
requests.packages.urllib3.disable_warnings()


url = "omitted for github"
url2 = "omitted for github"
url3 = "omitted for github"
headers = {'X-Auth-Token': ""}

response = requests.request("GET", url, headers=headers, verify=False).json()
response2 = requests.request("GET", url2, headers=headers, verify=False).json()
arrayDict = {}
diskList = []
for disk in response['items']:
    arrayDict[disk['deviceNumber']] = {}
    arrayDict[disk['deviceNumber']]['disks'] = []
    for disk in response2['items']:
        arrayDict[disk['deviceNumber']] = {}
        arrayDict[disk['deviceNumber']]['disks'] = []

for disk in response['items']:
    diskInfo = [disk['name'], disk['emcPartNumber'], disk['version']]
    arrayDict[disk['deviceNumber']]['disks'].append(diskInfo)

for disk in response2['items']:
    diskInfo = [disk['name'], disk['emcPartNumber'], disk['version']]
    arrayDict[disk['deviceNumber']]['disks'].append(diskInfo)

for array in arrayDict:
    response3 = requests.request(
        "GET", url3 + str(array), headers=headers, verify=False).json()
    arrayDict[array]['accountNumber'] = response3['accountNumber']
    arrayDict[array]['datacenter'] = response3['datacenter']
    arrayDict[array]['name'] = response3['name']
    arrayDict[array]['model'] = response3['model']


with open('list.csv', 'w') as csvfile:
    fieldnames = ['accountNumber', 'datacenter', 'deviceNumber',
                   'arrayName', 'arrayModel', 'diskName', 'emcPartNumber', 'version']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    for array in arrayDict:
        for disk in arrayDict[array]['disks']:
            writer.writerow([arrayDict[array]['accountNumber'],
                             arrayDict[array]['datacenter'], str(array),
                             arrayDict[array]['name'],
                             arrayDict[array]['model'], disk[0], disk[1], disk[2]])
    csvfile.close()
