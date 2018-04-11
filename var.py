#Use:
#python var.py [data].txt [column]
#

import numpy as np
import sys

def mean(a):
    sum = 0
    for i in a:
        sum += i
    sum = sum/a.size
    return sum

def var(a):
    Mean = mean(a)
    sum = 0
    for i in a:
        sum += (i-Mean)**2
    sum = sum/a.size
    sum = sum/(a.size - 1)
    return np.sqrt(sum)

data = np.genfromtxt(str(sys.argv[1]), unpack=True)

#print(data[int(sys.argv[2])])
if(data[0].size == 1):
    print(mean(data), "+/-", var(data), sep="")
else:
    print(mean(data[int(sys.argv[2])]), "+/-", var(data[int(sys.argv[2])]), sep="")
