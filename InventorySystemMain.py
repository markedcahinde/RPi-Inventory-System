import serial
import time
import sys
import sqlite3
import os
import gammu
import picamera
from datetime import datetime

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
conn = sqlite3.connect('/home/pi/Inventory System/DBs/InventorySystem.db')

os.system("clear")

try:
	while True:
		currentTime = time.strftime("%Y-%m-%d %a %H:%M:%S", time.localtime())
		ser.flushInput()
		rfidData = ser.readline().strip()
		str_rfidData = rfidData.encode('hex')
		if len(str_rfidData) == 0:
			print "Waiting for response..."

		else:
			print "Reader triggered! Checking db for existence of ", str_rfidData
			curs = conn.cursor()
			curs.execute('SELECT ITEM, BRAND FROM INVENTORY WHERE TAG = ?', (str_rfidData, ))
			result = curs.fetchone()

			if result:
				print "Taking snapshot..."
				i = datetime.now()
				now = i.strftime('%Y%m%d-%H%M%S')
				camera = picamera.PiCamera()
				camera.capture('/home/pi/snapshots/' + now + '.jpg')

				print "Item that triggered the reader was: "
				curs.execute('SELECT ITEM, BRAND FROM INVENTORY WHERE TAG = ?', (str_rfidData, ))
				for row in curs:
					print row
				conn.commit()
				curs.close()
				
				print "Card was found in db! Immediately contacting administrator..."
				sm = gammu.StateMachine()
				sm.ReadConfig()
				sm.Init()
				message = {
					'Text' : 'Alert! The Reader was triggered! A photo was captured and stored at /home/pi/snapshots.',
					'SMSC' : {'Location' : 1},
					'Number' : '09367713227'
				}
				sm.SendSMS(message)

except KeyboardInterrupt:
	print "Caught interrupt, exiting..."

except:
	print "Unexpected error: ", sys.exc_info()[0]

finally:
	ser.close()
