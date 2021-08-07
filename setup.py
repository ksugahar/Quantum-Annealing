from distutils.core import setup, Extension

setup(name = 'Hamiltonian', version = '1.0.0', ext_modules = [Extension('Hamiltonian', ['hamiltonian.c'])])