from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='IBITNormalizer',
    version='1.2.1',
    author='MahdiGhaemi',
    author_email='mahdighaemi123@gmail.com',
    description='Normalizer for persian texts base on hazm',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mahdighaemi123/IBITNormalizer',
    packages=find_packages(),
    package_data={'IBITNormalizer': ['resource/*']},
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
