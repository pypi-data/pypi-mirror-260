from setuptools import setup, find_packages

setup(
    name='aparat_crawler',
    version='0.8.7',
    packages=find_packages(),
    author='Mohammad Amin Orojloo',
    author_email='ma.orojloo@gmail.com',
    description='this is an aparat crawler library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/maorojloo/aparat_crawler',
    install_requires=[
        'beautifulsoup4==4.12.3',
        'persian==0.5.0',
        'requests==2.31.0',
        'aiohttp==3.8.6',
        'aiohttp-socks==0.8.4',

    ],
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
)
