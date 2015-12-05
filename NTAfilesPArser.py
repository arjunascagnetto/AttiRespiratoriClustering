import numpy as np
from collections import deque

filename = '001_ServoCurveData_0000.nta'

f = open(filename,'r')

lines = f.readlines()
data = deque()

for line in lines:
	if not line.startswith('%'):
		data.append(line.replace('\n','').split('\t',8))

v = np.ndarray(shape=(len(data),8),dtype=float)

print data[0]

for i in range(len(data)):
	for j in range(3,7):
		
		v[i,j]=float(data[i][j])
		print v[i,j],'\n',j
print v[:,1]
