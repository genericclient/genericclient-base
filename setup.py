import os
from setuptools import setup, find_packages

VERSION = '0.0.1'


f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='genericclient-base',
    version=VERSION,
    description='https://github.com/fcurella/genericclient-base',
    long_description=readme,
    author='Flavio Curella',
    author_email='flavio.curella@gmail.com',
    url='https://github.com/fcurella/genericclient-base',
    license='MIT License',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
    ],
    test_suite='tests',
    tests_require=[
        "coveralls",
        "mock",
    ]
)
