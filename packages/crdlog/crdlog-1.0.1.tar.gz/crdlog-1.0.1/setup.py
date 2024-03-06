from setuptools import setup, find_packages

setup(
    name='crdlog',
    version='1.0.1',
    packages=find_packages(),
    description='customed logging for simple scientific computing',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    install_requires=[
        'datetime',
        'colorlog',
    ]
)
