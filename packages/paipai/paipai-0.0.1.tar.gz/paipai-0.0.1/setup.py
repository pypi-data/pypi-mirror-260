# -*- encoding: UTF-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
import io

VERSION = '0.0.1'

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()

install_requires = open("requirements.txt").readlines()

setup(
    name="paipai",
    version=VERSION,
    author="yale",
    author_email="royal8848@163.com",
    url="https://github.com/yale8848/paipai",
    description="pip plus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["paipai"],
    package_data={},
    include_package_data=True,
    license='MIT License',
    classifiers=[],
    python_requires=">=3.6",
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'paipai=paipai.main:main'
        ]
    },
)