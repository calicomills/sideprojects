

#Author : Jishnu Chingum Kuniyil



import Tkinter as tk 
from Tkinter import *
import ttk
import subprocess
import time
from threading import Thread


 
relay_num = "651273"   

relay_num = "7529"   
relay_num = "651272"  
print relay_num


def activaterelay(port,relayOn) :
        cmd = 'C:\AutoTest\workspace\ctp2018\ps_est_ctp\lib\DTSI_Power\USBswitchCmd.exe -n'+ ' ' + relay_num + ' -# ' + port + ' ' + str(relayOn.get())
        print cmd
        time.sleep(2)
        print 'Turning ON relay'
        subprocess.call(cmd)  
def allopen():
        for i in range(0,8) :
           cmd = 'C:\AutoTest\workspace\ctp2018\ps_est_ctp\lib\DTSI_Power\USBswitchCmd.exe -n'+ ' ' + relay_num + ' -# ' + str(i) + ' ' + '0'
           print cmd
           time.sleep(0.5)
           print 'Turning OFF relay'
           subprocess.call(cmd) 
           relayOn_1.set(0)
           relayOn_2.set(0)
           relayOn_3.set(0)
           relayOn_4.set(0)
           relayOn_5.set(0)
           relayOn_6.set(0)
           relayOn_7.set(0)
           relayOn_8.set(0)
mroot = tk.Tk()
mroot.title("Cleware control tool:"+ relay_num)   #title
mroot.minsize(400,40)#size
Folder_label = Label(mroot,text="Ports",font=("Arial Bold", 10))
Folder_label.place(x = 10,y = 100)
open_button = Button(mroot,text="All open",font=("Arial Bold", 10),command=lambda : Thread(target = allopen).start() )
open_button.place(x = 300,y = 80, width=60, height=25)

relayOn_1= IntVar()
relayOn_2= IntVar()
relayOn_3= IntVar()
relayOn_4= IntVar()
relayOn_5= IntVar()
relayOn_6= IntVar()
relayOn_7= IntVar()
relayOn_8= IntVar()

check = ttk.Checkbutton(mroot, text=1,variable=relayOn_1, command=lambda : Thread(target = activaterelay,args= (str(0),relayOn_1)).start())
check.place(x = 10+1*40,y = 160)
check = ttk.Checkbutton(mroot, text=2,variable=relayOn_2, command=lambda : Thread(target = activaterelay,args= (str(1),relayOn_2)).start())
check.place(x = 10+2*40,y = 160)
check = ttk.Checkbutton(mroot, text=3,variable=relayOn_3, command=lambda : Thread(target = activaterelay,args= (str(2),relayOn_3)).start())
check.place(x = 10+3*40,y = 160)
check = ttk.Checkbutton(mroot, text=4,variable=relayOn_4, command=lambda : Thread(target = activaterelay,args= (str(3),relayOn_4)).start())
check.place(x = 10+4*40,y = 160)
check = ttk.Checkbutton(mroot, text=5,variable=relayOn_5, command=lambda : Thread(target = activaterelay,args= (str(4),relayOn_5)).start())
check.place(x = 10+5*40,y = 160)
check = ttk.Checkbutton(mroot, text=6,variable=relayOn_6, command=lambda : Thread(target = activaterelay,args= (str(5),relayOn_6)).start())
check.place(x = 10+6*40,y = 160)
check = ttk.Checkbutton(mroot, text=7,variable=relayOn_7, command=lambda : Thread(target = activaterelay,args= (str(6),relayOn_7)).start())
check.place(x = 10+7*40,y = 160)
check = ttk.Checkbutton(mroot, text=8,variable=relayOn_8, command=lambda : Thread(target = activaterelay,args= (str(7),relayOn_8)).start())
check.place(x = 10+8*40,y = 160)

mroot.mainloop() 
