from setuptools import setup, find_packages

setup(
    name='enigma_aps',
    version='1.0.2',
    packages=find_packages(),
    py_modules=['enigma_funcoes'],
    url='https://github.com/gabrielfmendesm/enigma_aps',
    license='MIT',
    author='Gabriel Mendes',
    author_email='gabrielfmm@al.insper.edu.br',
    description='Uma biblioteca que contém funções para cifrar e decifrar mensagens usando uma simulação da máquina enigma.',
)
