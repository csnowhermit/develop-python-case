import time

'''
    斐波那契数列：python
'''

def fib(n):
    if not isinstance(n, int):
        raise ValueError('n is incorrect')
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

if __name__ == '__main__':
    start = time.time()
    print(fib(30))
    print("耗时：", time.time() - start)