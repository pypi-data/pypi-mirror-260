from setuptools import setup

setup(
    name='tnsname_formatter',  
    version='0.1.0',  
    description='A tool to format TNSnames files and download them as Excel files containing Server name and Database name',
    author='Tarun Kesavan Menon',
    author_email='tarunmenon383@example.com',
    install_requires=['pandas', 'openpyxl'],  
    py_modules=['ServeExl'],  
)