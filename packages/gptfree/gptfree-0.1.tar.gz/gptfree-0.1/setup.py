from setuptools import setup, find_packages

setup(
    name='gptfree',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.7.4',  
    ],
    author='Syo',
    author_email='syojp9999@gmail.com',
    description='A simple wrapper for GPT-free API.',
    keywords='GPT API',
)