import subprocess
from datetime import datetime
import os
import shutil

def run_triiage(spa_filename, spb_filename, device_number):
    today = datetime.today()
    #dir_name = device_number + ' ' + today.strftime('%c %x')
    dir_name = device_number + today.strftime('_%m.%d.%y_%H.%M.%S')
    os.makedirs(dir_name, exist_ok=True)
    shutil.move(spa_filename, dir_name)
    shutil.move(spb_filename, dir_name)
    subprocess.Popen('triage', cwd=dir_name)

run_triiage('SPA_data.zip', 'SPB_data.zip', '987654')
