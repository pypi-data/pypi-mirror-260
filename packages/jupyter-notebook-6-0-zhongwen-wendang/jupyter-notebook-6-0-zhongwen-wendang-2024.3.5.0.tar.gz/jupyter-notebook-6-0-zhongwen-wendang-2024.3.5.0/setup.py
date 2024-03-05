#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import JupyterNotebook60ZhongwenWendang
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('JupyterNotebook60ZhongwenWendang'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="jupyter-notebook-6-0-zhongwen-wendang",
    version=JupyterNotebook60ZhongwenWendang.__version__,
    url="https://github.com/apachecn/jupyter-notebook-6-0-zhongwen-wendang",
    author=JupyterNotebook60ZhongwenWendang.__author__,
    author_email=JupyterNotebook60ZhongwenWendang.__email__,
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
    description="Jupyter Notebook 6.0 中文文档",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "jupyter-notebook-6-0-zhongwen-wendang=JupyterNotebook60ZhongwenWendang.__main__:main",
            "JupyterNotebook60ZhongwenWendang=JupyterNotebook60ZhongwenWendang.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
