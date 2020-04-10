import time
import numpy as np
cimport cython
cimport numpy as np    # 用来引入.pxd文件（相当于c/c++中的头文件）

'''
    矩阵相乘
'''

@cython.boundscheck(False)    # 关闭cython的边界检查
@cython.wraparound(False)
cdef np.ndarray[np.float32_t, ndim=2] _dot(np.ndarray[np.float32_t, ndim=2] m1, np.ndarray[np.float32_t, ndim=2] m2):
  cdef np.ndarray[np.float32_t, ndim=2] r    # 在函数内部, 我们可以使用cdef typename varname这样的语法来声明变量。
  cdef int i, j, k
  cdef np.float32_t s
  if m1.shape[1] != m2.shape[0]:
    raise ValueError('m1 and m2 dimension mismatch')
  r = np.zeros((m1.shape[0], m2.shape[1]), dtype=np.float32)
  for i in range(m1.shape[0]):
    for j in range(m2.shape[1]):
      s = 0
      for k in range(m1.shape[1]):
        s += m1[i, k] * m2[k, j]
      r[i, j] = s
  return r

def dot(m1, m2):
  return _dot(m1, m2)

if __name__ == '__main__':
    m1 = np.random.randn(100, 200)
    m2 = np.random.randn(200, 150)
    start = time.time()
    print(dot(m1, m2))
    print("耗时：", time.time() - start)

