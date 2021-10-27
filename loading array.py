# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 14:28:45 2021

@author: asus
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
N = int(input("square array size :")) #write down size of square array

lp = float(input("loading prop(1-100):")) # write down loading probability

#definitation sampling array
def sam(x):
    A = np.zeros([N, N], dtype = int)  #make an array from inputing size
    for i in range (0,N):
        for j in range(0,N):
            p = np.random.randint(1,101) #random number
            if p < lp :
                A[i,j] =1
            else:
                A[i,j] = 0
    return A

ns = int(input("number of sampling:"))
fisam = np.zeros([N, N])
df = pd.DataFrame(columns=['array'])               
for i in range (0,N):
    fisam += sam(i)
    df = df.append({'array': sam(i)}, ignore_index=True)
#





plt.imshow(fisam, interpolation='none',cmap='Blues')
plt.colorbar()
plt.show()
print(df) 