from setuptools import setup, find_packages

setup(
    name='cms-crypto',
    version='1.0.1',
    author='Rishabh Mehta',
    author_email='Rishabh2.Mehta@ril.com',
    description='CMS decryption helper package',
    url='https://github.com/fin1te/',
    packages=find_packages(),
    install_requires=[
        'requests',
        'loguru',
        'pycryptodome',
        'setuptools'
    ]
)