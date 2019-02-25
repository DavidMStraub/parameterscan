from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(name='parameterscan',
      version='0.1',
      author='David M. Straub',
      author_email='david.straub@tum.de',
      description='Python package for parameter scans',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      license='MIT',
      packages=find_packages(),
      install_requires=['pandas', 'numpy', 'sqlalchemy', 'schwimmbad'],
      )
