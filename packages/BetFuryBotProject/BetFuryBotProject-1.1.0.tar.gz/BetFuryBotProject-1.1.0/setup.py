from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='BetFuryBotProject',
  version='1.1.0',
  author='Kujira',
  author_email='nopemo93@gmail.com',
  description='Bet Fury Bot package',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/DreamBreakk/BetFuryBotProject',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.12',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='BetFuryBotProject',
  project_urls={
    'Documentation': 'https://github.com/DreamBreakk/BetFuryBotProject'
  },
  python_requires='>=3.7'
)