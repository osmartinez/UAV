import socket
from pymultiwii import MultiWii
import time

ip = ''
port = 5003
bufflen = 19
address= ("192.168.1.33",5000)
cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mon_socket  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dir =  ('',5003)
cmd_socket.bind((ip,port))

uav=MultiWii("/dev/ttyUSB0")
uav.arm()

time.sleep(5)

orden=[]


##orden={"roll":-1,"pitch":-1,"yaw":-1,"throttle":-1}

try:    
    while True:
        data,_ = cmd_socket.recvfrom(bufflen)
        data = data.split(':')

        if data == ['']:
            continue
        #print str(data)
        orden_s = [int(data[0]),int(data[1]),int(data[2]),int(data[3])]
        print orden_s
        if orden_s[3]==-2:
            print 'disarm command received'
            break
        if(orden_s!=orden):
            orden=orden_s
            #imu=uav.sendCMDreceiveATT(8,MultiWii.SET_RAW_RC,orden)
            uav.sendCMD(8,MultiWii.SET_RAW_RC,orden)
            ##message =str(uav.getData(MultiWii.ATTITUDE))
            ##mon_socket.sendto(message,address)
            #if imu!=None:
                #imu_socket.sendto(imu,dir)	
            ##print orden
        if not data: break
        
    cmd_socket.close()
    uav.disarm()
except KeyboardInterrupt:
    cmd_socket.close()
    uav.disarm()
except Exception as e:
    print str(e)
    cmd_socket.close()
    uav.disarm()

