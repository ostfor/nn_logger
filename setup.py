from setuptools import setup

name = "nn_logger"
pkgs = [name]
setup(name=name,
      version="0.1",
      description='Tool for logging for deep learning training process',
      author='Denis Brailovsky',
      author_email='denis.brailovsky@gmail.com',
      license='MIT',
      packages=pkgs,
      py_modules=['__init__'],
      zip_safe=False)
