from setuptools import setup, find_packages
setup(
name='mlxserver',
version='0.1.2',
author='Mustafa Aljadery',
author_email='aljadery@usc.edu',
description='Server using the MLX library.',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
],
python_requires='>=3.6',
)