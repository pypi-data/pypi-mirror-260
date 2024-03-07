from setuptools import setup, find_packages

setup(
    name='IBITNormalizer',
    version='1.2.5',
    description='Normalizer for Persian texts based on hazm',
    author='MahdiGhaemi',
    author_email='mahdighaemi123@email.com',
    packages=find_packages(), 
    package_data={'IBITNormalizer': ['resources/*']},
    include_package_data=True,
    install_requires=[], 
)
