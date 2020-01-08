import matplotlib.pyplot as plt # for plotting

import pandas as pd # for data handling
import numpy as np  # for calculations
import matplotlib


wine = pd.read_csv('wine_data.csv', delimiter=";")
#wine.head()
plt.figure()
'''
try:
    plt.hist(wine["class"])
except Exception as E:
    print E
'''  
    
#plt.show()

type2 = wine.loc[wine['class'] == 2]
'''
plt.rcParams["figure.figsize"] = (6,6)
plt.xlim([11,14])
print type2["alcohol"]
a = plt.hist(type2['alcohol'].values,15,normed = True)
plt.show()
'''
print np.var(type2['alcohol'])
print np.mean(type2['alcohol'])


mean = np.mean(type2['alcohol'])
print('Estimated mean:\n', '{:6.3f}'.format(mean))

# variance
var = np.var(type2['alcohol'])
print('\nEstimated variance: \n', '{:6.3f}'.format(var))

# Gauss plot
x1 = np.arange(10,14,0.01)
y1 = norm.pdf(x1,mean,var)
plt.plot(x1,y1, label = 'fitted curve')

# plot the distribution of the alcohol data
x  = a[1] # bin edges
x2 = x[1:] - (x[1]-x[0])/2 # shift to the middle of the bins
y2 = a[0]
plt.plot(x2,y2,'ro',label = 'input data')
plt.xlim([11,14])
plt.legend()
plt.show()


