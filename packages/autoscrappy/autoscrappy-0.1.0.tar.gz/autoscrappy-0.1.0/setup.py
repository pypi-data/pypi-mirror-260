from setuptools import find_packages,setup
setup(
    name='autoscrappy',
    packages=find_packages(include=['com','project','Logger','common','Scrapper','Logs']),
    version ='0.1.0',
    description='My first Python library',
    author='Me',
    install_requires=['beautifulsoup4==4.12.3','logging==0.4.9.6','setuptools','wrapt','twine','wheel']


)
