#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import ShiyongSpringCloudYuDockerShizhanWeiFuwu
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('ShiyongSpringCloudYuDockerShizhanWeiFuwu'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="shiyong-spring-cloud-yu-docker-shizhan-wei-fuwu",
    version=ShiyongSpringCloudYuDockerShizhanWeiFuwu.__version__,
    url="https://github.com/apachecn/shiyong-spring-cloud-yu-docker-shizhan-wei-fuwu",
    author=ShiyongSpringCloudYuDockerShizhanWeiFuwu.__author__,
    author_email=ShiyongSpringCloudYuDockerShizhanWeiFuwu.__email__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Documentation",
        "Topic :: Documentation",
    ],
    description="使用Spring Cloud与Docker实战微服务",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "shiyong-spring-cloud-yu-docker-shizhan-wei-fuwu=ShiyongSpringCloudYuDockerShizhanWeiFuwu.__main__:main",
            "ShiyongSpringCloudYuDockerShizhanWeiFuwu=ShiyongSpringCloudYuDockerShizhanWeiFuwu.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
