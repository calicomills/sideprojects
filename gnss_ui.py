import paramiko
import time
from threading import Thread
from Tkinter import *
import Queue
import Tkinter as tk


class GNSS(tk.Tk):
        def __init__(self):
            self.ssh_connection_target()
            tk.Tk.__init__(self)
            
            self.title('CTP tool') 
            self.configure(bg='alice blue')
            self.geometry("%dx%d+%d+%d" % (600, 665, 50, 50))
            self.resizable(width=False, height=False)
            Thread(target = self.GPS_config).start()
            button_stop = tk.Button(self, text='Stop', width=25, command=self.destroy) 
            button_stop.pack() 
            open_button = tk.Button(self,text="Date",font=("Arial Bold", 10),command=lambda : Thread(target = self.ssh_connection_target).start() )
            open_button.place(x = 300,y = 80, width=60, height=25)
            open_button.pack()   
            self.time_update()
            
            button_GPS = tk.Button(self, text='GNSS_config', width=25, command=lambda : Thread(target = self.GPS_set).start()) 
            button_GPS.place(x = 500,y = 80, width=60, height=25)
            button_GPS.pack()
            
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

                
        def label(self):
                    print "Fetching time"
                    self.ssh_connection_target()
                    self.var1 = StringVar()
                    self.var1.set(self.t)
                    w = Label(self, bg='alice blue',textvariable=self.var1)
                    w.pack()
                    while True:
                        self.ssh_connection_target()
                        self.var1.set(self.t)
                       
                    #w.after(240, lambda : w.destroy())
                
        def time_update(self):
                 Thread(target = self.label).start()
                 
        def GPS_config(self):
            ssh = self.ssh_connection_target()
            stdin,stdout,stderr = ssh.exec_command(' cat /data/signed/topas_platform.conf | grep GNSS_CONFIG | cut -c 13-16')
            output=stdout.readlines()
            self.gnss_config = output[0]
            self.var = StringVar()
            self.var.set(self.gnss_config)
            w = Label(self, bg='red',textvariable=self.var)
            w.pack()   
            
        def GPS_set(self):
            ssh = self.ssh_connection_target()
            stdin,stdout,stderr = ssh.exec_command(' cat /data/signed/topas_platform.conf | grep GNSS_CONFIG | cut -c 13-16')
            output=stdout.readlines()
            self.gnss_config = output[0]
            self.var = StringVar()
            self.var.set(self.gnss_config)
            
                    

GNSS().mainloop()


