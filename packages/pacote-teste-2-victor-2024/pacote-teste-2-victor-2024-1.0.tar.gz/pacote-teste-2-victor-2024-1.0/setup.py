from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='pacote-teste-2-victor-2024',
    version=1.0,
    description='Pacote de teste para aprender a criar pacotes',
    long_description=Path('README.md').read_text(),
    author='Victor Donizete',
    author_email='victordonizete65@gmail.com',
    keywords=['teste', 'teste2', 'invalido'],
    packages=find_packages()
)