from setuptools import setup, find_packages

setup(
    name='Get_Link_Src_Count',
    version='1.0.0',
    description='A package that get total link src',
    author='Your Name',
    author_email='manangondez@gmail.com',
    packages=find_packages(),
    install_requires=[
        'web-assets-downloader',
        'requests',
        'beautifulsoup4'
    ],
)