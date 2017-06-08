import socket
from wifi import Cell,Scheme

val = Cell.all('wlan0');

ap_list = []

for v in val:
    if v.ssid not in ap_list:
        ap_list.append(v.ssid)
        print v.ssid," ",v.address
        print "\n"

TCP_IP = '192.168.20.17'
TCP1_IP = '192.168.18.214'
TCP_PORT = 30

Bufsize = 1024
M = "S"
M2 = '1C5CF206D44b'.decode('hex')
# Message  = M+M2

Message = 'B'

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))
s.send(Message)
date =s.recv(1024)
s.close()


print "sent",date

