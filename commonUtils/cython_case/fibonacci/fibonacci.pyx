import time
import cython

'''
    斐波那契数列：cython加速
    和Fibonacci.py一样，只是后缀名不同
    怎样调用？
        （1）编译Cython代码，并生成对应的动态链接库；
        （2）Python解释器载入动态链接库。

    Note:
        （1）@cython.boundscheck(False)和cython.wraparound(False)：关闭Cython的边界检查。
        （2）cdef：定义函数, 并且可以给所有参数以及返回值指定类型。
        （3）def：因为在python程序中, 我们是看不到cdef函数的, 所以我们这里要再用def定义一个fib函数, 来调用cdef的_fib函数。
'''

@cython.boundscheck(False)    # 关闭Cython的边界检查
@cython.wraparound(False)
cdef int _fib(int n):
  if not isinstance(n, int):
    raise ValueError('n is incorrect')
  if n <= 1: return n
  return fib(n-1) + fib(n-2)

def fib(n):
  return _fib(n)
