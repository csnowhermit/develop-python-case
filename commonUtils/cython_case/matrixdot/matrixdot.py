import time
import numpy as np

'''
    矩阵相乘
'''

def dot(m1, m2):
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

if __name__ == '__main__':
    m1 = np.random.randn(100, 200)
    m2 = np.random.randn(200, 150)
    start = time.time()
    print(dot(m1, m2))
    print("耗时：", time.time() - start)

