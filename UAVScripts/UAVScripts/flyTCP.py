import socket
from pymultiwii import MultiWii
import time

ip = ''
port = 5003
bufflen = 19
imu_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dir =  ("192.168.1.34",5000)
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip,port))

uav=MultiWii("/dev/ttyUSB0")
uav.arm()
try:
    time.sleep(10)

    s.listen(1)
    print 'Escuchando conexiones...'
    conn,addr = s.accept()
    print 'Conexion aceptada: '+str(addr)
except KeyboardInterrupt:
    uav.disarm()
orden=[]


##orden={"roll":-1,"pitch":-1,"yaw":-1,"throttle":-1}

try:    
    while True:
        data = conn.recv(bufflen)
        ##data = data.replace('\r\n','')
        data = data.split(':')
        if data == ['']:
            continue
        print str(data)
        orden_s = [int(data[0]),int(data[1]),int(data[2]),int(data[3])]
        
        if orden_s[3]==0:
            print 'orden de desarme recibida'
            break
        if(orden_s!=orden):
            orden=orden_s

            ##cuidado que no le entre la orden con algun -1
            #imu=uav.sendCMDreceiveATT(8,MultiWii.SET_RAW_RC,orden)
            uav.sendCMD(8,MultiWii.SET_RAW_RC,orden)
            #if imu!=None:
                #imu_socket.sendto(imu,dir)	
            ##print orden
        if not data: break
        
    conn.close()
    uav.disarm()
except KeyboardInterrupt:
    conn.close()
    uav.disarm()
except Exception as e:
    print str(e)
    conn.close()
    uav.disarm()
