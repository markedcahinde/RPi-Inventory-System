import serial
import time
import sqlite3
import os

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
conn = sqlite3.connect('/home/pi/InventorySystem/DBs/InventorySystem.db')
curs = conn.cursor()

os.system("clear")

print "Use this module only if a new item is to be added to the database."
print " This will only scan the tag."
print " To add the unit and brand, open the web browser and go to localhost."
raw_input("Press Enter to continue and Ctrl+C to terminate...")

try:
	while True:
		ser.flushInput()
		string = ser.readline().strip()
		if len(string) == 0:
			print "Please put the tag near the reader..."
			continue
		else:
			str = string.encode('hex')
			name = ' '
			brand = ' '
			curs.execute('INSERT INTO INVENTORY VALUES (?, ?, ?)', (str, name, brand))
			print "Successfully added to db!"
			conn.commit()
			for row in curs.execute('SELECT * FROM INVENTORY'):
				print row
			time.sleep(1)
			ser.flushInput()

except KeyboardInterrupt:
	print "Program interrupted. Exiting..."

finally:
	conn.close()
	ser.close()
