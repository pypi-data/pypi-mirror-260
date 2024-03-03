from setuptools import find_packages, setup

VERSION = '0.1.0'
DESCRIPTION = 'A Python package for automated error notification emails, enhancing software debugging and maintenance.'

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='EmailErrorMix',
    version=VERSION,
    author='Mathimix',
    author_email="<mathimixich@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(include=['EmailErrorMix']),
    install_requires=[],
    license="MIT",
    url="https://github.com/Mathimix7/EmailErrorMix",
    keywords=['python', 'email', 'error', 'alerts', 'maintenance'],
    long_description = long_description,
    long_description_content_type = "text/markdown",
)
