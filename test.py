#!/usr/bin/env python
import serial
import time
import signal
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
# ============================================================================
# ============================================================================
class SignalException(Exception):
         pass

def signal_term_handler(signal, frame):
     print('got SIGTERM')
     raise SignalException('SIGTERM')

def print_timestamp():
         print(time.strftime("%Y-%m-%d %H:%M:%S"))

# ============================================================================
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        signal.signal(signal.SIGTERM, signal_term_handler)

        ser.write(b"\n")
        sensor_data=ser.readline()

        self.wfile.write(sensor_data)
        save_file()

        return
# ============================================================================
def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()

# ============================================================================
def save_file():
    port_adress = ser.name

    file = open('data.txt', 'a')
    file.write("PORT ADRESS \t")
    file.write(port_adress)
    file.write("\n\nSENSOR DATA: \n")

    for i in range(1, 5):
        ser.write(b"\n")    # send sth to arduino
        sensor_data=ser.readline()
        file.write(time.asctime())
        file.write("\t")
        file.write(str(sensor_data))
        file.write("\n")
        time.sleep(5)     # one measurement every 60s
    file.write("\n\n")
    file.close()
    print(time.asctime() )
    print("saved to file data.txt\n")

    return

# ============================================================================
signal.signal(signal.SIGTERM, signal_term_handler)
ser = serial.Serial('/dev/ttyACM0' , 9600, timeout=2)
time.sleep(2)

run()
ser.close()
