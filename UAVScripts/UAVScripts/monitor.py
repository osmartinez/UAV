from pymultiwii import MultiWii
from sys import stdout
import socket

class Monitor():
    def __init__(self, direccion, port):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._address = (direccion,port)

    def run(self):
	self._board = MultiWii('/dev/ttyUSB0')
        while True:
            try:
                message =str(self._board.getData(MultiWii.ATTITUDE))
		print message
		self._s.sendto(message,self._address)		
            except KeyboardInterrupt:
                print 'Liberando socket...'
                self._s.close()
                break

import sys

def error():
    print 'Error: Wrong arguments!'
    print 'Use: python <script> <port> <ip>'
    time.sleep(4)
    exit()

def main():
    args = sys.argv
    if len(args)!=3:
        error()

    port = -1
    ip = ""
    try:
        port = int(args[1])
	ip = args[2]
    except Exception as ex:
        print str(ex)
    
    mon = Monitor(ip,port)
    mon.ejecutar()

if __name__ == "__main__": main()

