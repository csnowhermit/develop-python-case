# setup_dot.py
import numpy
from Cython.Build import cythonize
from distutils.core import setup, Extension

setup(
  ext_modules=cythonize(Extension('matrixdot_cython',
                  sources=['matrixdot.pyx'],
                  language='c',
                  include_dirs=[numpy.get_include()],
                  library_dirs=[],
                  libraries=[],
                  extra_compile_args=[],
                  extra_link_args=[]))
)