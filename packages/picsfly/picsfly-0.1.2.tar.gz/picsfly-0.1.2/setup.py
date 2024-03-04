from setuptools import setup

setup(
    name='picsfly',
    version='0.1.2',
    packages=['picsfly'],
    install_requires=[
        'pywin32',
        'pycryptodome',
        'requests',
    ],
)
