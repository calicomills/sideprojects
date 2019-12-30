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




class GNSS(tk.Tk):
    def __init__(self):
        Thread(target=self.get_cpu_load).start()
        tk.Tk.__init__(self)
        self.title('CTP tool')
        self.configure(bg='alice blue')
        self.geometry("%dx%d+%d+%d" % (600, 665, 50, 50))
        self.resizable(width=False, height=False)
        style = ttk.Style()
        style.map("C.TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')]
                  )
        open_button = ttk.Button(self, text="CTP", command=lambda: Thread(target=self.print_something).start(),style = "C.TButton")
        open_button.pack()

        self.f = Figure(figsize=(5, 5), dpi=100, )
        self.a = self.f.add_subplot(111)
        #self.f.xlabel("Time")
        

        canvas = FigureCanvasTkAgg(self.f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.ani = animation.FuncAnimation(self.f, self.animate, interval=10)

    def animate(self,i):
        
        yList = self.uniload
        xList = self.time
        
        self.a.clear()
        self.a.set_ylim(0,100)
        self.a.set_ylabel("Load")
        self.a.set_xlabel("Time")
        self.a.plot(xList, yList)
        
        

    def ssh_connection_target(self):
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect('192.168.1.40', username='root', password='ctp1fb',timeout=20)
                print "waiting_for_ssh_connection"
                #time.sleep(2)
                #print "Going to shut down"
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
                '''
                self.var = StringVar()
                self.var.set(self.cpuload)
                w = Label(self, bg='red',textvariable=self.var)
                w.pack()    
                ''' 
                now = datetime.now().strftime("%H:%M:%S")
                print now
                h,m,s=now.split(':')
                sec=float(h)*3600+float(m)*60+float(s)
                sec = int(sec)
    
                self.uniload.append(int(self.cpuload))
                self.time.append(int(sec))
            except Exception as E:
                print E
                self.uniload.append(int(0))
                now = datetime.now().strftime("%H:%M:%S")
                print now
                h,m,s=now.split(':')
                sec=float(h)*3600+float(m)*60+float(s)
                sec = int(sec)
                self.time.append(int(sec))
    def print_something(self):
        print "Button pressed!"
        
        
    def exit_prgm(self):
        self.quit()
        self.destroy()
        print "Doneeeeeeeeeeee"
        os._exit(0)



GNSS().mainloop()
os._exit(0)
