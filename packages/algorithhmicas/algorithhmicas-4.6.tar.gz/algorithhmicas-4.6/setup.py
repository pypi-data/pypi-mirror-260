from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        print('HELLO2')  # Move this line before install.run(self)
        install.run(self)
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION

setup(
    name='algorithhmicas',
    version='4.6',
    author='Your Name',
    author_email='cinnabonwithcinnamon@email.com',
    description='Description of library',
    packages=['algorithhmicas'],
    install_requires=[
        'numpy', 'requests'
    ],
    cmdclass={
        'install': PostInstallCommand,
    }
)