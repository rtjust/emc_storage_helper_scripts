import requests
from lxml import html

requests.packages.urllib3.disable_warnings()
r1 = requests.post('https://ip_address/setup/login', data = {'Username':'user', 'Password':'pass','method':'navisphere','Language':''}, verify=False)
page = r1
tree = html.fromstring(page.content)
token = tree.xpath('//input[@name="SecurityToken"]/@value')
r3 = requests.post('https://ip_address/setup/setAutomanage', data = {'AutoManage':'Disable', 'SecurityToken':token,'Language':''}, verify=False)
