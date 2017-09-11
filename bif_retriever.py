import os
import time
import datetime

import utils

sys_conf_path = 'C:\\Program Files (x86)\\Trend Micro\\Control Manager\\SystemConfiguration.xml'
log_processor_config_path = 'C:\\Program Files (x86)\\Trend Micro\\Control Manager\\LogProcessor.exe.config'
log_path = 'C:\\Program Files (x86)\\Trend Micro\\Control Manager\\DebugLog\\TMCM_LogProcessor.log'
output = 'bif.xml'
t_start = None

def get_proper_time():
    global t_start
    delta_minutes = 1
    if int(datetime.datetime.now().strftime('%S')) >= 55:
        delta_minutes += 1
    t_start = datetime.datetime.now() + datetime.timedelta(minutes=delta_minutes)
    return t_start.strftime('%H:%M:00')

def check_time(line):
    format = '%Y-%m-%d %H:%M:%S'
    time_str = line[:19]
    t = None
    try:
        t = datetime.datetime.strptime(time_str, format)
    except:
        return False
    return t >= t_start

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

utils.setAttribute(sys_conf_path, ".//P[@Name='%s']" % 'm_BIFConnectRepeatIntervalInDays', "Value", '1')
utils.setAttribute(sys_conf_path, ".//P[@Name='%s']" % 'm_BIFConnectStartTime', "Value", get_proper_time())
utils.setAttribute(log_processor_config_path, ".//priority", "value", 'DEBUG')

os.system("taskkill /F /im LogProcessor.exe")

result = ''
f = open(log_path, 'r')
lines = follow(f)
for line in lines:
    if 'BIFXml Info' in line:
        result = line
        break
if result != '':
    f.close()

result = result[result.find('<'):result.rfind('>') + 1]

with open(output, 'w') as f:
    f.write(result)
os.startfile(output)