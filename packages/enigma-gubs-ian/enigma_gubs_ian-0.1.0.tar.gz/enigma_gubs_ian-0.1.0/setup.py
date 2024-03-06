from setuptools import setup, find_packages

setup(
    name='enigma_gubs_ian',
    packages=find_packages(include=['enigma_gubs_ian']),
    version='0.1.0',
    description='Enigma machine linear algebra implementation',
    author='Gubs and Ian',
    install_requires=['numpy', 'flask'],
)