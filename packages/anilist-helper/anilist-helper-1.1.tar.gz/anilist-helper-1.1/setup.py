from setuptools import setup, find_packages
setup(
    name='anilist-helper',
    version='1.01',
    description='A Python library to fetch data from Anilist',
    author='Dominik Procházka',
    packages=find_packages(),
    package_data={'': ['token_getter.html']},
    install_requires=['flask', 'gevent', 'requests']
)