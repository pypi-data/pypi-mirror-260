from distutils.core import setup
import setuptools
packages = ['file_ls']
setup(name='file_ls',
    version='1.0.0',
    author='唐旭东',
    packages=packages,
    package_dir={'requests': 'requests'},
    install_requires=[
        "natsort"
    ])