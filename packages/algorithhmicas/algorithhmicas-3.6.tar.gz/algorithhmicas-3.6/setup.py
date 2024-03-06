from setuptools import setup
from setuptools.command.install import install
import os

class CustomInstallCommand(install):
    """Customized setuptools install command - runs a script after installing the module."""
    def run(self):
        install.run(self)
        os.system('echo "Hello World"')
        print("fdsafsadfsdfsdfsdfsdf")

setup(
    version='3.6',
    author='Your Name',
    author_email='cinnabonwithcinnamon@email.com',
    description='Description of library',
    packages=['algorithhmicas'],
    install_requires=[
        'numpy', 'requests'
    ],
    cmdclass={
        'install': CustomInstallCommand,
    }
)