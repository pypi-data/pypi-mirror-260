from setuptools import setup, find_packages
import os

version = os.getenv('VERSION', '0.1.0') # Usa la versión del tag o 0.1 como predeterminado

# requirements from requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='brian_lib',
    version=version,
    packages=find_packages(),
    install_requires=required,
    python_requires='>=3.8'
)
