import time
import matplotlib
matplotlib.use('TKAgg',warn=False, force=True)
from threading import Thread
from Tkinter import *
import Tkinter as tk
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import random
import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np







class GNSS(tk.Tk):
    def __init__(self):
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
        open_button = ttk.Button(self, text="Hello world", command=lambda: Thread(target=self.print_something).start(),style = "C.TButton")
        open_button.pack()

        self.f = Figure(figsize=(5, 5), dpi=100)
        self.a = self.f.add_subplot(111)

        canvas = FigureCanvasTkAgg(self.f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.ani = animation.FuncAnimation(self.f, self.animate, interval=2000)

    def animate(self,i):
        pullData = open("sample.txt", "r").read()
        dataList = pullData.split('\n')
        print dataList
        xList = []
        yList = []

        for eachLine in dataList:
            if len(eachLine) > 1 and i > 0:
                x, y = eachLine.split(',')
                xList.append(int(x))
                yList.append(int(y))

                self.a.clear()
                self.a.plot(xList, yList)
                i = i-1
                print x,y

        '''
        print "i",i

        xList = np.arange(i,i+100)
        print xList
        yList = np.sin(xList / 10)


        self.a.clear()
        self.a.plot(xList, yList)
        '''

    def print_something(self):
        print "Button pressed!"
    def exit_prgm(self):
        self.quit()
        self.destroy()
        print "Doneeeeeeeeeeee"
        os._exit(0)



GNSS().mainloop()
os._exit(0)
