#!/usr/bin/python
import os
from os import listdir
import sys
import time
import random
import subprocess
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

print "Script start"
#set up adb and aapt path, and test apks dir
apksDir = "/home/yu/ADATF/apks/"
adb = "/home/yu/android-sdks/platform-tools/adb"
aapt = "/home/yu/android-sdks/build-tools/18.0.1/aapt"
#start adb
os.system(adb + " start-server")
if os.path.exists("results") == False:
	os.mkdir("results")
# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
print "Device connected"

#get device display width and height
width = int (device.getProperty('display.width'))
height = int (device.getProperty('display.height'))

#for all apk in aoksDir
for file in listdir(apksDir):
	#print file
	#read apkinfo
	apkinfo = os.popen(aapt + " d badging " + apksDir + file)
	apkinfo = apkinfo.read()
	#get apkname
	start = apkinfo.find("package")
	end = apkinfo.find("versionCode", start)
	apkpackage = apkinfo[start : end - 1]
	apkname = apkpackage[apkpackage.find("'") + 1 : apkpackage.rfind("'")]
	#get launch activity
	start = apkinfo.find("launchable-activity")
	end = apkinfo.find("label", start)
	apkactivity = apkinfo[start : end - 1]
	apkactivity = apkactivity[apkactivity.find("'") + 1 : apkactivity.rfind("'")]
	
	#install apk
	print "install " + file
	os.system(adb + " install " + apksDir + file)
	#start activity
	timeformat = "%y_%m_%d-%X"
	logFileName = "TEST_" + time.strftime(timeformat)
	netdir = "results/" + apkname + "_" + logFileName + "_network_traffic.pcap"
	subprocess.Popen("tcpdump -i eth0 -w " + netdir + "&", shell=True)
	print "Start cap network"
	print "start activity " + apkactivity
	device.startActivity(component=apkname + "/" + apkactivity)
	time.sleep(10)
	#send touch event at any point on the screen
	x = 0
	y = 0
	print "touch screen"
	while x < width:
		while y < height:
			device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
			#sleep after one touch
			time.sleep(1)
			#drag the screen
			x1 = random.randint(0, width)
			y1 = random.randint(0, height)
			x2 = random.randint(0, width)
			y2 = random.randint(0, height)
			device.drag((x1, y1), (x2, y2), 1.0, 10)
			time.sleep(1)
			y = y + 10
		x = x + 10
	#send touch event of any key on the screen
	#KeyEvent ref:http://developer.android.com/reference/android/view/KeyEvent.html
	print "press screen"
	device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)	#press the menu key
	#print "unistall apk"
	#unistall apk
	#os.system(adb + " uninstall " + apkname)
