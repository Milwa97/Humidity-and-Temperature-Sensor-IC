#!/usr/bin/python
import serial
import time
import signal
import sys
#import json
# ============================================================================
class SignalException(Exception):
         pass

def signal_term_handler(signal, frame):
     print('got SIGTERM')
     raise SignalException('SIGTERM')

def print_timestamp():
         print(time.strftime("%Y-%m-%d %H:%M:%S"))

# ============================================================================
signal.signal(signal.SIGTERM, signal_term_handler)

ser = serial.Serial('/dev/ttyACM0' , 9600, timeout=2)
port_adress = ser.name
time.sleep(2)

error_counter = 0

file = open('data.txt', 'w')
file.write("PORT ADRESS \t")
file.write(port_adress)
file.write("\n\nDATA: \n\n")

print("done I")
# ============================================================================
while True:
         try:
                # with open('/home/pi/light/light.json') as json_data:
                #         d = json.load(json_data)
                #         red = d[u'red']
                #         green = d[u'green']
                #         yellow = d[u'yellow']
                 ser.write("\n")    # send sth to arduino
                 x=ser.readline()
                 time.sleep(60)     # one measurement every 60s
                 file.write(time.asctime())
                 file.write("\t")
                 file.write(x)
                 file.write("\n")

                 error_counter = 0

         except KeyboardInterrupt:
                 print("Keybord Interrupt caught")
                 break
         except SignalException:
                 print("SIGTERM caught")
                 break
         except Exception as e:
                 print("Other exception caught: %s" % str(e))
                 print_timestamp()
                 error_counter = error_counter + 1
                 time.sleep(5)
                 if error_counter > 5:
                         break
print("done II")

file.close()
#ser.close()
print("Exit")


# press ... to stop
# show resulst
# save and exit
