from setuptools import find_packages, setup

setup(
    name='samplescrap',
    packages=find_packages(),
    version='0.1.0',
    description='My first Python library',
    author='Me',
    install_requires=['beautifulsoup4==4.12.3', 'logging==0.4.9.6', 'setuptools', 'wrapt', 'twine', 'wheel']
)
