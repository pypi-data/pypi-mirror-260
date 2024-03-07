from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(name='IBITNormalizer',
      packages=[''],
      version='1.2.3',
      description='Normalizer for persian texts base on hazm',
      author='MahdiGhaemi',
      author_email='',
      url='https://github.com/mahdighaemi123/IBITNormalizer',
      download_url='',
      python_requires=">=3.3",
      classifiers=[],
      include_package_data=True,
      long_description=long_description,
      long_description_content_type='text/markdown',
      )
