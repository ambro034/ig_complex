from setuptools import setup

setup(
  name = 'ig_complex',
  version = '0.0.1',
  description = "A package used to identify complexity in policy statements",
  url = 'https://github.com/ambro034/text_reuse.git',
  author_name = 'Graham W. Ambrose',
  license = 'unlicense',
  package = ['ig_complex'],
  install_requires=['spacy',
                   'svglib',
                   'pandas',
                   'pandas',
                   'python-Levenshtein']
  
)
  
