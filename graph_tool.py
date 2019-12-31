import time
import matplotlib
matplotlib.use('TKAgg',warn=False, force=True)
from threading import Thread
from Tkinter import *
import Tkinter as tk
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import random
import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np
import paramiko
from datetime import datetime
import serial




class GNSS(tk.Tk):
    def __init__(self):
        self.current = []
        self.timetoel = []
        Thread(target=self.get_cpu_load).start()
        self.time_update()
        Thread(target=self.SW_ver_config).start()
        #Thread(target=self.get_current).start()
        

        tk.Tk.__init__(self)
        self.title('CTP tool')
        self.configure(bg='alice blue')
        self.geometry("%dx%d+%d+%d" % (800, 600, 50, 50))
        #self.resizable(width=False, height=False)
        style = ttk.Style()
        style.map("C.TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')]
                  )
        
        
        open_button = ttk.Button(self, text="CTP", command=lambda: Thread(target=self.print_something).start(),style = "C.TButton")
        open_button.place(x = 600,y = 30, width=75, height=30)
        

        exit_button = ttk.Button(self, text="Quit", command=self.exit_prgm,style = "C.TButton")
        exit_button.place(x = 675,y = 30, width=75, height=30)
        
                    
        button_GPS = tk.Button(self, text='GNSS_config', width=25, command=lambda : Thread(target = self.GPS_set).start()) 
        button_GPS.place(x = 100,y = 300, width=60, height=25)
       
        
        button_ver = tk.Button(self, text='SW version', width=25, command=self.SW_ver_config_set) 
        button_ver.place(x = 180,y = 30, width=70, height=25)
        
        
        self.f = Figure(figsize=(5, 3), dpi=100,)
        self.a = self.f.add_subplot(111)
        

        canvas = FigureCanvasTkAgg(self.f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=0)

        self.ani = animation.FuncAnimation(self.f, self.animate, interval=10)

    def animate(self,i):
        
        yList1 = self.uniload[len(self.uniload)-5:len(self.uniload)-1]
        yList = self.uniload
        xList = self.time[len(self.time)-5:len(self.time)-1]
        xList2 = self.time
        zList = self.current[len(self.current)-5:len(self.current)-1]
        zList = self.current
        xList1 = self.timetoel[len(self.timetoel)-5:len(self.timetoel)-1]
        xList3 = self.timetoel
        
        self.a.clear()
        #self.a.set_ylim(0,100)
        self.a.set_ylabel("Load")
        self.a.set_xlabel("Time")
        self.a.plot(xList2, yList)
        self.a.plot(xList3, zList)
        
        

    def ssh_connection_target(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.1.40', username='root', password='ctp1fb',timeout=20)
            print "waiting_for_ssh_connection"
            stdin,stdout,stderr = ssh.exec_command('date')
            output=stdout.readlines()
            print output
            self.t = output[0]
            return ssh            
        except Exception as E:
            print E
                
                
    def get_cpu_load(self):
        self.uniload = []
        self.time = []
        while True:
            try:
                ssh = self.ssh_connection_target()
                stdin,stdout,stderr = ssh.exec_command(" grep 'cpu ' /proc/stat | awk '{usage=($2+$3+$4+$7+$8+$9)*100/($2+$3+$4+$5+$6+$7+$8+$9)} END {print usage}'")
                output=stdout.readlines()
                print output[0].rstrip()
                self.cpuload = float(str(output[0].rstrip()))
                
                now = datetime.now().strftime("%H:%M:%S")
                print now
                h,m,s=now.split(':')
                sec=float(h)*3600+float(m)*60+float(s)
                sec = int(sec)
    
                self.uniload.append(int(self.cpuload))
                self.time.append(int(sec))
                self.get_current()
            except Exception as E:
                print E
                self.uniload.append(int(0))
                now = datetime.now().strftime("%H:%M:%S")
                print now
                h,m,s=now.split(':')
                sec=float(h)*3600+float(m)*60+float(s)
                sec = int(sec)
                self.time.append(int(sec))
                self.get_current()
                

    def print_something(self):
        print "Button pressed!"
        
        
    def label(self):
        self.ssh_connection_target()
        self.var1 = StringVar()
        self.var1.set(self.t)
        w = Label(self, bg='alice blue',textvariable=self.var1)
        w.place(x = 380,y = 30, width=200, height=30)
        while True:
            self.ssh_connection_target()
            self.var1.set(self.t)
                        
    def time_update(self):
        Thread(target = self.label).start() 
        
    def GPS_set(self):
        ssh = self.ssh_connection_target()
        stdin,stdout,stderr = ssh.exec_command(' cat /data/signed/topas_platform.conf | grep GNSS_CONFIG | cut -c 13-16')
        output=stdout.readlines()
        self.gnss_config = output[0]
        self.var = StringVar()
        self.var.set(self.gnss_config)
    
    def SW_ver_config(self):
        ssh = self.ssh_connection_target()
        stdin,stdout,stderr = ssh.exec_command('cat /etc/topas/version_project.cfg')
        output=stdout.readlines()
        self.project_ver = output[0]
        self.var2 = StringVar()
        self.var2.set(self.project_ver)
        w = Label(self,textvariable=self.var2)
        w.place(x = 250,y = 30, width=150, height=30)
            
    def SW_ver_config_set(self):
        ssh = self.ssh_connection_target()
        stdin,stdout,stderr = ssh.exec_command('cat /etc/topas/version_project.cfg')
        output=stdout.readlines()
        self.project_ver = output[0]
        self.var2 = StringVar()
        self.var2.set(self.project_ver)
        
    def get_current(self):
         try:
                 s = serial.Serial('COM1',9600,timeout=20)
                 if s.isOpen():
                     print(s.name + ' is open...')
                 cmd = 'SYST:REM'
                 cmd2 = 'INST:NSEL 1'
                 cmd3 = 'MEAS:CURR:DC?'
                 s.write(cmd.encode('ascii')+'\r\n')
                 s.write(cmd2.encode('ascii') +'\r\n' )
                 s.write(cmd3.encode('ascii') +'\r\n' )
    
                 res = s.readline()
                 s.close()
                 curr = float(res)*1000
                 self.current.append(int(curr))
                 now = datetime.now().strftime("%H:%M:%S")
                 print now
                 h,m,s=now.split(':')
                 sec=float(h)*3600+float(m)*60+float(s)
                 sec = int(sec)
                 self.timetoel.append(sec)
                 
     
         except Exception as E:
                print E
                if len(self.current) > 0 :
                    self.current.append(self.current[len(self.current)-1])
                else :
                    self.current.append(0)
                now = datetime.now().strftime("%H:%M:%S")
                print now
                h,m,s=now.split(':')
                sec=float(h)*3600+float(m)*60+float(s)
                sec = int(sec)
                self.timetoel.append(sec)
                  

    
    def exit_prgm(self):
        self.quit()
        self.destroy()
        print "Exiting Program"
        os._exit(0)



GNSS().mainloop()
os._exit(0)
