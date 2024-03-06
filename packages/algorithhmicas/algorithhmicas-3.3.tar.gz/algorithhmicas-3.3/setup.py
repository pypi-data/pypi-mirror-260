from setuptools import setup, find_packages

setup(
    name='algorithhmicas',
    version='3.3',
    author='Your Name',
    author_email='cinnabonwithcinnamon@email.com',
    description='Description of library',
    packages=find_packages(),
    install_requires=[
        'numpy', 'requests'
    ],
    entry_points={
        'console_scripts': [
            'my_program=algorighhmicas.module1:main_function'
        ],
    }
)