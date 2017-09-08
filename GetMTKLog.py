#coding:utf-8
import os
import datetime
import time
import re

adbpath = os.getcwd()+'\\adb.exe'

def getDeviceName():
    curpath=os.getcwd()
    dev = getDevices()
    os.system(adbpath+' -s '+dev[0]+' shell \"getprop | grep ro.product.name\">'+'\"'+curpath+'\"'+"\\attr.log")
    with open(curpath+"\\attr.log") as attr:
        for line in attr:
            if re.match(r'\[\w+\.\w+\.\w+]:\s+\[(\w+)\]',line):
                product_name = re.match('\[\w+\.\w+\.\w+]:\s+\[(\w+)\]',line).group(1)
                return product_name

def getCurrentTime(formats):
    #%Y%m%d%H%M%S
    now=datetime.datetime.now()
    newTime=now.strftime(formats)
    return newTime

def newFolder(path,curtime):
    cpath=path+"\\"+curtime
    if not os.path.exists(cpath):
        os.makedirs(cpath)
    return cpath
    
def getDevices():
    device = []
    curpath = os.getcwd()
    os.system(adbpath+' devices>'+'\"'+curpath+'\"'+"\\device.info")
    with open(curpath+'\\device.info') as data:
        for line in data:
            dev = re.match(r'\w{16}',line)
            if dev:
                device.append(dev.group())
    return device
                
def startLog(s_number):
    os.system(adbpath+' -s '+s_number+' shell am broadcast -a com.mediatek.mtklogger.ADB_CMD -e cmd_name start --ei cmd_target 7')
    print (s_number+'_ Start MTKlog Succeed')
    
def stopLog(s_number):   
    os.system(adbpath+' -s '+s_number+' shell am broadcast -a com.mediatek.mtklogger.ADB_CMD -e cmd_name stop --ei cmd_target 7')
    print (s_number+'_ Stop MTKlog Succeed')
        
def deleteLog(s_number):
    os.system(adbpath+' -s '+s_number+' shell rm -rf /mnt/m_internal_storage/mtklog')
    time.sleep(2)
    print (s_number+'_ Delete MTKlog Succeed')
    
def pullLog(s_number,path):
    curtime=getCurrentTime("%Y%m%d_%H%M")
    logpath =  path+'\\'+s_number
    c_logpath = newFolder(logpath,curtime)
    os.system(adbpath+' -s '+s_number+' pull /mnt/m_internal_storage/mtklog/ '+'\"'+c_logpath+'\"')  
	os.system(adbpath+' -s '+s_number+' shell'+' \"dumpsys meminfo >'+c_logpath+'\\memoinfo.txt\"')  
    print(s_number+'_ Pull log Succeed')
    


if __name__ == '__main__':
    
    total_time=int(raw_input('Please Enter Total time: '))
    mean_time=int(raw_input('Please Enter interval time: '))
    devices = getDevices()
    path = os.getcwd()+'\\mtklog'
    logpath = path+'\\'+getDeviceName()
    if not os.path.exists(logpath):
        os.makedirs(logpath)

    for a in range(len(devices)):
        os.system(adbpath+' -s '+devices[a]+' shell setprop persist.mtklog.log2sd.path /mnt/m_internal_storage')
        print (devices[a]+'_ Set MTKlog location as Internal storage')
        stopLog(devices[a])
        time.sleep(2)
        deleteLog(devices[a])
        time.sleep(10)
        
    loop_time=total_time/mean_time+1
    for b in range(loop_time):
        for c in range(len(devices)):
            startLog(devices[c])
        time.sleep(mean_time*60)
        for d in range(len(devices)):
            stopLog(devices[d])
            time.sleep(2)
            pullLog(devices[d],logpath)
            time.sleep(10)
            deleteLog(devices[d])
    for anr in range(len(devices)):
        os.system(adbpath+' -s '+devices[anr] +' pull /data/anr/ '+'\"'+logpath+'\\'+devices[anr]+'\\'+'ANR'+'\"')
        print (str(devices[anr])+" anrlog pull success")


