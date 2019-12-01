######################################################################################
#        Code      :    Simulation of Inspection Paradox                             # 
#        Author    :    Jishnu Chingum Kuniyil                                       #
#        Dept      :    RBEI/ECG1                                                    #
#        Date      :    27-07-2019 16:00:00                                          #
###################################################################################### 


import random
import matplotlib.pyplot as plt
import time
import math

class inspection:
    def __init__(self):
        self.list=[]
        self.count = [0]*16
    def sample_creation(self,num_samples):
        for i in range(1,num_samples):
            size=random.randint(10,15)
            j=size
            while(j>0):
                self.list.append(size)
                j-=1
            self.list.append('A')
        print self.list       
            
    def find_problty(self,num_trials):
        for chance in range(1,num_trials):
             select=random.randint(1,len(self.list)-1)
             #print select
             if self.list[select] == 'A':
                 chance-=1
                 
           
             num = select
             if self.list[num] != 'A':
                 if num == len(self.list)-2:
                    self.count[1]+=1
                 else:
                     while(num < len(self.list)-1):          
                         if self.list[num+1] == 'A':
                             time_int = abs(select - (num+1))
                             self.count[time_int]+=1
                             #print time_int
                             break
                         num += 1  
           

        print self.count 
        count = [float(c) / num_trials*100 for c in self.count]
        print self.count
        x_axis=range(1,16)
        print x_axis
        y_axis=count[1:]
        print y_axis   
        return x_axis,y_axis
    
obj = inspection()  
obj.sample_creation(100) 
x_axis,y_axis = obj.find_problty(10) 
print 'Plotting graph'
plt.ylabel('Percentage of occurence')
plt.xlabel('Waiting intervals')
plt.plot(x_axis,y_axis,'blue') 
plt.show() 
