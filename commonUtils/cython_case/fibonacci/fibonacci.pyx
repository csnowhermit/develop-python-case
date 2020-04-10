import time

'''
    斐波那契数列：cython加速
    和Fibonacci.py一样，只是后缀名不同
    怎样调用？
        （1）编译Cython代码，并生成对应的动态链接库；
        （2）Python解释器载入动态链接库。
'''

def fib(n):
    if not isinstance(n, int):
        raise ValueError('n is incorrect')
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

if __name__ == '__main__':
    start = time.time()
    print(fib(100))
    print("耗时：", time.time() - start)