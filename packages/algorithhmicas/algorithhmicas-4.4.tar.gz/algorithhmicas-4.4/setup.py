from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        print("HELLO1")
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        print('HELLO2')
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION

setup(
    name='algorithhmicas',
    version='4.4',
    author='Your Name',
    author_email='cinnabonwithcinnamon@email.com',
    description='Description of library',
    packages=['algorithhmicas'],
    install_requires=[
        'numpy', 'requests'
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    }
)