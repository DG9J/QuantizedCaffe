import numpy as np
a = np.array([1, 2, 3])
print a.shape

a = np.array([[1,2], [3,4], [5,6]])
bool_idx = (a > 2)
print bool_idx
print a[bool_idx]
print a[a>2]

x = np.array([[1,2],[3,4]])
y = np.array([[5,6],[7,8]])

v = np.array([9,10])
w = np.array([11, 12])

# Inner product of vectors; both produce 219
print v.dot(w)
print np.dot(v, w)