import time
import string
import matplotlib.pyplot as plt
import math


t0 = 1
k = 25
n =  range(1,100)
t = []



for i in n:
   t.append(t0 * math.exp(i) / k)


print t

plt.plot(n,t,'blue')

 

plt.ylabel('Time to travel')
plt.xlabel('No. of vehicles / time')
plt.show()