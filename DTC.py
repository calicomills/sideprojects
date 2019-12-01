import socket
import time

host = "192.168.1.40"
port = 11115
s = []
d = []

Channels = ["POWER","CAN1","CAN2","CAN3","D8","DAIO","MODEM","GPS","DIAG","CFGMGR","RTC","SYSTEMDIAG","BACKEND","BLE","WIFI","SECURITY","UPDATE","AUDIO","INVALID"]

for i in range(len(Channels)):
   s.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
   d.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
   
try:
   for i in range(0,len(Channels)):
      s[i].connect((host, port))
      d[i].connect((host, port))
      channel =   Channels[i] + " FB"
      channel_d = Channels[i] + " RDA"
      s[i].sendall(channel.upper())
      data = s[i].recv(1024)
      print Channels[i],data
      if Channels[i] in Channels:
         d[i].sendall(channel_d.upper())
         data = d[i].recv(1024)
         print Channels[i],data
except Exception,e:
   print e

time.sleep(30)
   

