from setuptools import setup, find_packages

setup(
    name='test-automation-cms',
    version='1.0.0',
    author='Rishabh Mehta',
    author_email='Rishabh2.Mehta@ril.com',
    description='Testing automatic upload',
    url='https://github.com/fin1te/',
    packages=find_packages(),
    install_requires=[
        'requests',
        'loguru',
        'pycryptodome',
        'setuptools'
    ]
)