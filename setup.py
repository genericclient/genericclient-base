import os
from setuptools import setup, find_packages

VERSION = '1.0.1'


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

setup(
    name='genericclient-base',
    version=VERSION,
    description='',
    long_description=readme,
    author='Flavio Curella',
    author_email='flavio.curella@gmail.com',
    url='https://github.com/genericclient/genericclient-base',
    license='MIT License',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        "attrs>=17.4.0",
    ],
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=[
        "coveralls",
        "pytest",
        "mock",
    ]
)
