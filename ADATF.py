#!/usr/bin/python
import os
from os import listdir
import sys
import time
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

print "Script start"
#set up adb and aapt path, and test apks dir
apksDir = "D:/Src/Android/apks/"
adb = "Absolute path of sdk->platform-tools->adb"
aapt = "Absolute path of sdk->build-tools->android-4.4->aapt"
#start adb
os.system(adb + " start-server")

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
print "Device connected"

#get device display width and height
width = device.getProperty('display.width')
height = device.getProperty('display.height')

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
	print "start activity " + apkactivity
	device.startActivity(component=apkname + "/" + apkactivity)
	time.sleep(10)
	#send touch event at any point on the screen
	'''
	x = 0
	y = 0
	print "touch screen"
	while x < width:
		while y < height:
			#print "Touch " + str(x) + ", " + str(y)
			device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
			#sleep after one touch
			time.sleep(1)
			y = y + 1
		x = x + 1
	'''
	#send touch event of any key on the screen
	#KeyEvent ref:http://developer.android.com/reference/android/view/KeyEvent.html
	print "press screen"
	device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)	#press the menu key
	
	#send drag event between any point on the screen
	print "drag screen"
	device.drag((50, 50), (300, 300), 1.0, 10)
	
	print "unistall apk"
	#unistall apk
	os.system(adb + " uninstall " + apkname)