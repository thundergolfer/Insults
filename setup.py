import os
from distutils.core import setup
from setuptools import find_packages
from support.commands.py_test import UnitTest

def get_pip_dependencies():
    this_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(this_dir, 'requirements.txt'), 'r') as pip_requirements:
        package_list = [package for package in pip_requirements]
    return package_list

setup(
  name = 'insults',
  packages = find_packages(exclude=['scripts', 'docs', 'tests*']),
  version = '0.1.9',
  description = 'Identify insulting comments and users on social media',
  author = 'Jonathon Belotti',
  author_email = 'jonathon.bel.melbourne@gmail.com',
  url = 'https://github.com/thundergolfer/Insults', # use the URL to the github repo
  download_url = 'https://github.com/thundergolfer/Insult/tarball/0.1', # I'll explain this in a second
  keywords = ['machine-learning', 'social-media', 'community', 'data-science'], # arbitrary keywords
  classifiers = [],
  install_requires = [
        'pyparsing==1.5.6',
        'python-dateutil==2.4.1',
        'pytest==3.0.6',
        'Pytz==2016.7',
        'scikit-learn==0.18.1',
        'scipy==0.18.1',
        'six==1.10.0',
        'pandas==0.19.2',
        'futures==2.2.0',
        'nltk==3.0'
  ],
  cmdclass = {'unit': UnitTest }
)

## FOR download_url
# The download_url is a link to a hosted file with your repository's code.
# Github will host this for you, but only if you create a git tag.
# In your repository, type:
# git tag 0.1 -m "Adds a tag so that we can put this on PyPI.".
# Then, type git tag to show a list of tags. you should see 0.1 in the list.
# Type git push --tags origin master to update your code on Github with the latest tag information. Github creates tarballs for download at https://github.com/{username}/{module_name}/tarball/{tag}.
