import paramiko
import time
from threading import Thread
from Tkinter import *
import Queue
import Tkinter as tk
import sys,os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

class GNSS(tk.Tk):
        def __init__(self):
            self.ssh_connection_target()
            tk.Tk.__init__(self)
            
            self.title('CTP tool') 
            
         
            self.configure(bg='alice blue')
            self.geometry("%dx%d+%d+%d" % (600, 665, 50, 50))
            self.resizable(width=False, height=False)
            Thread(target = self.GPS_config).start()
            self.SW_ver_config() 
            open_button = tk.Button(self,text="Date",font=("Arial Bold", 10),command=lambda : Thread(target = self.ssh_connection_target).start() )
            open_button.place(x = 300,y = 80, width=60, height=25)
            open_button.pack()   
            self.time_update()
            
            button_GPS = tk.Button(self, text='GNSS_config', width=25, command=lambda : Thread(target = self.GPS_set).start()) 
            button_GPS.place(x = 500,y = 80, width=60, height=25)
            button_GPS.pack()
            
            button_ver = tk.Button(self, text='SW version', width=25, command=self.SW_ver_config_set()) 
            button_ver.place(x = 400,y = 80, width=60, height=25)
            button_ver.pack()
            
            button_stop = tk.Button(self, text='Stop', width=25, command=self.exit_prgm) 
            button_stop.pack()
          
            
            
            
        #def plot(self):      
            fig = Figure(figsize=(1, 1), dpi=100)
            t = np.arange(0, 3, .01)
            fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
            canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            toolbar = NavigationToolbar2TkAgg(canvas, self)
            toolbar.update()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)       
            #toolbar = NavigationToolbar2TkAgg(canvas, self)
            #toolbar.update()
            #canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            
     
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
            
        def SW_ver_config(self):
            ssh = self.ssh_connection_target()
            stdin,stdout,stderr = ssh.exec_command('cat /etc/topas/version_project.cfg')
            output=stdout.readlines()
            self.project_ver = output[0]
            self.var2 = StringVar()
            self.var2.set(self.project_ver)
            w = Label(self, bg='red',textvariable=self.var2)
            w.pack()   
            
        def SW_ver_config_set(self):
            ssh = self.ssh_connection_target()
            stdin,stdout,stderr = ssh.exec_command('cat /etc/topas/version_project.cfg')
            output=stdout.readlines()
            self.project_ver = output[0]
            self.var2 = StringVar()
            self.var2.set(self.project_ver)
            
        def exit_prgm(self):
            self.quit()
            self.destroy()    
            print "Doneeeeeeeeeeee"
            os._exit(0)
            
                

GNSS().mainloop()
os._exit(0)

