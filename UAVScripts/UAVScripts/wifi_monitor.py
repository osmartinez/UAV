import sys
import subprocess
import time
import socket

class WifiMonitor():
    def __init__(self, interfaz, ip, port):
        self._interfaz = interfaz
        self._nombre_red = self.get_nombre_red().strip()
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._dir = (ip,port)


    def get_canal(self,celda):
        troceada = celda.split('Channel:')
        canal = troceada[1][0]+troceada[1][1]
        return canal

    def get_calidad(self,celda):
        troceada = celda.split('Quality=')
        calidad= troceada[1][0:5]
        return calidad

    def get_intensidad(self,celda):
        troceada=celda.split('Signal level=')
        intensidad=troceada[1][0:3]
        return intensidad

    def get_nombre_red(self):
        proc = subprocess.Popen(["iwgetid", "-r"],stdout=subprocess.PIPE, universal_newlines=True)
        out, _= proc.communicate()
        return out

    def ejecutar(self):
        while True:
            try:
                proc = subprocess.Popen(["iwlist", self._interfaz, "scan"],stdout=subprocess.PIPE, universal_newlines=True)
                out,_=proc.communicate()

                mi_celda = ""
                out_troceado = out.split('Cell')
                for cell in out_troceado:
                    if self._nombre_red in cell:
                        mi_celda = cell
                        break
                if mi_celda=="":
                    time.sleep(5)
                    continue
                canal = self.get_canal(mi_celda)
                calidad = self.get_calidad(mi_celda)
                intensidad = self.get_intensidad(mi_celda)

                paquete = self._nombre_red+" "+canal+" "+calidad+" "+intensidad
                self._s.sendto(paquete,self._dir)
                time.sleep(1)
            except Exception as ex:
                self._s.close()
                print ex
                break

import sys

def error():
    print 'Error: Wrong arguments!'
    print 'Use: python <script> <interfaz_red> <port> <ip>'
    time.sleep(4)
    exit()

def main():
    args = sys.argv
    if len(args)!=4:
        error()

    iface = ""
    port = -1
    ip = ""
    try:
	iface = args[1]
        port = int(args[2])
	ip = args[3]
    except Exception as ex:
        print str(ex)
    
    wifi_mon = WifiMonitor(iface,ip,port)
    wifi_mon.ejecutar()

if __name__ == "__main__": main()
