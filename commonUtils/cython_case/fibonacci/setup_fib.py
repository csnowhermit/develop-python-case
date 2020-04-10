# setup_fib.py
from Cython.Build import cythonize
from distutils.core import setup, Extension

'''
    怎样调用pyx？
        （1）编译Cython代码（生成.c文件），并生成对应的动态链接库（该脚本进行第一步的步骤）；
            调用方法：python setup_fib.py build_ext --inplace
        （2）Python解释器载入动态链接库。
'''

setup(
  ext_modules=cythonize(Extension('fibonacci_cython',    # 生成的动态链接库名字
                  sources=['fibonacci.pyx'],    # 需要的包括.pyx和.c/.cpp文件
                  language='c',        # 默认是c，也可以是c++
                  include_dirs=[],     # gcc -I 参数
                  library_dirs=[],     # gcc -L 参数
                  libraries=[],        # gcc -l 参数
                  extra_compile_args=["-DPLATFORM=linux"],    # 传给gcc的额外编译参数
                  extra_link_args=[]))      # 传给gcc的额外链接参数
)