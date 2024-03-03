from setuptools import find_packages, setup

VERSION = '0.0.1'
DESCRIPTION = 'A Python package for automated error notification emails, enhancing software debugging and maintenance.'

setup(
    name='EmailErrorMix',
    version=VERSION,
    author='Mathimix',
    author_email="<mathimixich@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(include=['EmailErrorMix']),
    install_requires=[],
    keywords=['python', 'email', 'error', 'alerts', 'maintenance'],
)