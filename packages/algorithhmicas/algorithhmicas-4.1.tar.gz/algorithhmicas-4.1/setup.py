from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class CustomInstallCommand(install):
    """Customized setuptools install command - runs a script after installing the module."""
    def run(self):
        install.run(self)
        print("hello world")  # Этот код выполнится при установке пакета

setup(
    name='algorithhmicas',
    version='4.1',
    author='Your Name',
    author_email='cinnabonwithcinnamon@email.com',
    description='Description of library',
    packages=find_packages(),
    install_requires=[
        'numpy', 'requests'
    ],
    cmdclass={
        'install': CustomInstallCommand,
    }
)