from setuptools import setup, find_packages


setup(
    name='zer0poc',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask==3.0.2',
        'Requests==2.31.0'
    ],
    license='MIT',
    description='PoC generater thats fast and pretty for your vulnerabilty.',
    long_description=open('README.md').read(),
    url='https://github.com/retr0reg/zer00poc',
    author='0reg',
    author_email='0reg@0reg.dev'
)