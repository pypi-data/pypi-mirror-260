# setup.py

from setuptools import setup, find_packages

setup(
    name='darkhorsesapi',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # Add your project's dependencies here
        # e.g., 'requests', 'pandas',
    ],
    author='Craig Carmichael',
    author_email='operations@darkhorsestech.com',
    description='An API client library for Dark Horses API.',
    license='MIT',
    url='https://github.com/darkhorsestech/darkhorsesapi',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
