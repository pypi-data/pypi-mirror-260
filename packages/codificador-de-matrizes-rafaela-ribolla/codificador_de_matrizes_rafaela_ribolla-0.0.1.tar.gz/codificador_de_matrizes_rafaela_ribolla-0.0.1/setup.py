from setuptools import setup, find_packages

from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='codificador_de_matrizes_rafaela_ribolla',
    version='0.0.1',
    license='MIT License',
    author='Rafaela Afférri e Gustavo Ribolla',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='rafaelaao@al.insper.edu.br',
    keywords='matriz',
    description=u'Codificador de matrizes',
    packages=['codificador_de_matrizes_rafaela_ribolla'],
    install_requires=['numpy'],)



